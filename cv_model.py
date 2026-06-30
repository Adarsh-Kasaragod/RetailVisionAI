import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions

# Load the pre-trained MobileNetV2 model
# This model is pre-trained on the ImageNet dataset (1000 classes), 
# which contains many retail products (bottles, cups, laptops, clothes, etc.)
print("Loading MobileNetV2 model...")
model = MobileNetV2(weights='imagenet')
print("Model loaded successfully.")

def preprocess_image(image_path):
    """
    Use OpenCV to read and preprocess the image before feeding it to TensorFlow.
    """
    # 1. Read image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read the image.")

    # 2. Convert from BGR (OpenCV default) to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 3. Resize to 224x224 (MobileNetV2 expected input size)
    img = cv2.resize(img, (224, 224))

    # 4. Convert to numpy array and add batch dimension (1, 224, 224, 3)
    img_array = np.expand_dims(img, axis=0)

    # 5. Preprocess the input specifically for MobileNetV2 (scales pixels to [-1, 1])
    processed_img = preprocess_input(img_array)

    return processed_img

def predict_product(image_path):
    """
    Predict the class of the product in the image.
    Returns the top prediction label and its confidence score.
    """
    try:
        # Preprocess the image
        processed_img = preprocess_image(image_path)
        
        # Run inference
        predictions = model.predict(processed_img)
        
        # Decode predictions (get top 1)
        # Returns a list of lists: [[(class_name, class_description, score), ...]]
        decoded = decode_predictions(predictions, top=1)[0][0]
        
        class_id, class_name, confidence = decoded
        
        # Clean up class name (replace underscores with spaces and title case it)
        clean_name = class_name.replace('_', ' ').title()
        confidence_pct = float(confidence) * 100
        
        return clean_name, confidence_pct
        
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        return None, 0.0
