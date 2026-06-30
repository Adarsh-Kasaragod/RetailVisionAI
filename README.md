# RetailVision AI 🚀

RetailVision AI is a robust, AI-powered web application that classifies retail product images using Deep Learning and Computer Vision. It allows users to upload images of retail products and instantly receive highly accurate classifications along with confidence scores.

This project was built to demonstrate end-to-end AI engineering skills, including model integration, image preprocessing, backend API development, database management, and responsive UI design.

## Features ✨

* **Deep Learning Inference:** Utilizes a pre-trained **TensorFlow/Keras MobileNetV2** model for fast and accurate image classification.
* **Computer Vision Preprocessing:** Uses **OpenCV** to read, resize, and convert images to the correct color spaces before feeding them into the neural network.
* **Prediction History & Dashboard:** Automatically logs all predictions (image path, predicted class, confidence score, timestamp) into an **SQLite** database and displays them on a dashboard.
* **Modern Web Interface:** A responsive, sleek UI built with HTML/CSS and Vanilla JS featuring drag-and-drop file uploads, image previews, and smooth loading animations.
* **RESTful Backend API:** Powered by **Flask**, handling file validation, storage, and connecting the frontend to the AI model seamlessly.

## Tech Stack 🛠️

* **Backend:** Python 3, Flask, Werkzeug
* **AI/ML:** TensorFlow, Keras, OpenCV, NumPy
* **Database:** SQLite
* **Frontend:** HTML5, CSS3, JavaScript (AJAX)

## Quick Start (How to Run Locally) 💻

### Prerequisites
Make sure you have Python 3.8+ installed on your system.

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/RetailVision_AI.git
cd RetailVision_AI
```

### 2. Set up a virtual environment (Recommended)
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
*(Note: Installing TensorFlow may take a few moments depending on your network speed)*

### 4. Run the application
```bash
python app.py
```

### 5. Access the Web App
Open your browser and navigate to:
`http://localhost:5000`

## Project Structure 📁
```text
RetailVision_AI/
│
├── app.py                 # Main Flask application and routing
├── database.py            # SQLite database initialization and queries
├── cv_model.py            # TensorFlow model loading and OpenCV preprocessing
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
│
├── static/
│   ├── css/style.css      # Custom responsive styling
│   ├── js/main.js         # Frontend logic (Image preview, AJAX uploads)
│   └── uploads/           # Directory where uploaded images are saved
│
└── templates/
    ├── base.html          # Base layout template
    ├── index.html         # Main upload and prediction interface
    └── dashboard.html     # Prediction history dashboard
```

## How the AI Works 🧠

1. **Upload:** User uploads an image via the web UI. The image is passed via AJAX to the Flask backend.
2. **Preprocessing (OpenCV):** The image is read by OpenCV (`cv2.imread`), converted from BGR to RGB (`cv2.cvtColor`), and resized to `224x224` pixels to match the input requirements of MobileNetV2.
3. **Inference (TensorFlow):** The preprocessed image array is fed into the loaded MobileNetV2 model.
4. **Post-processing:** The model outputs a probability distribution. We decode the top prediction to get the human-readable class name and calculate the confidence percentage.
5. **Storage:** The result is saved into the SQLite database.
6. **Response:** The frontend receives the JSON response and updates the UI.

## License
MIT License
