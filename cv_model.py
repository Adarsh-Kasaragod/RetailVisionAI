import cv2
import numpy as np
import random
import time

try:
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    
    # Load the pre-trained MobileNetV2 model
    print("Loading MobileNetV2 model...")
    model = MobileNetV2(weights='imagenet')
    print("Model loaded successfully.")
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("WARNING: TensorFlow is not installed (likely due to Python 3.14 incompatibility).")
    print("Running in MOCK mode for UI demonstration purposes.")
    TENSORFLOW_AVAILABLE = False

def preprocess_image(image_path):
    """
    Use OpenCV to read and preprocess the image.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read the image.")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    
    if TENSORFLOW_AVAILABLE:
        img_array = np.expand_dims(img, axis=0)
        processed_img = preprocess_input(img_array)
        return processed_img
    return img

def predict_product(image_path):
    """
    Predict the class of the product in the image.
    """
    try:
        if not TENSORFLOW_AVAILABLE:
            # MOCK MODE FOR DEMONSTRATION
            time.sleep(1.5) # Simulate processing time
            mock_products = ['Water Bottle', 'Coffee Mug', 'Computer Mouse', 'Laptop Computer', 'Backpack']
            return random.choice(mock_products), random.uniform(75.0, 99.9)

        # REAL TENSORFLOW INFERENCE
        processed_img = preprocess_image(image_path)
        predictions = model.predict(processed_img)
        decoded = decode_predictions(predictions, top=1)[0][0]
        class_id, class_name, confidence = decoded
        
        clean_name = class_name.replace('_', ' ').title()
        confidence_pct = float(confidence) * 100
        return clean_name, confidence_pct
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return None, 0.0
