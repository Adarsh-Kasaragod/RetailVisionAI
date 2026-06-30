import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import database
import cv_model

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize database
database.init_db()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render the main upload page."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render the dashboard with prediction history."""
    history = database.get_recent_predictions(limit=20)
    return render_template('dashboard.html', history=history)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to handle image upload and return prediction."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file to disk
        file.save(filepath)
        
        # Run prediction via OpenCV and TensorFlow
        predicted_class, confidence = cv_model.predict_product(filepath)
        
        if predicted_class:
            # Save to database
            database.save_prediction(filename, predicted_class, confidence)
            
            return jsonify({
                'success': True,
                'prediction': predicted_class,
                'confidence': round(confidence, 2),
                'image_url': f'/static/uploads/{filename}'
            })
        else:
            return jsonify({'error': 'Failed to process image.'}), 500
            
    return jsonify({'error': 'Invalid file type. Only JPG, PNG, and WEBP are allowed.'}), 400

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True, port=5000)
