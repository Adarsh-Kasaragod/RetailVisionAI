# RetailVision AI

This is a personal project I built to practice my computer vision and deep learning skills. It's a web application where you can upload an image of a retail product, and it will classify what the product is.

I built the backend using Python and Flask, and I used a pre-trained TensorFlow MobileNetV2 model for the classification so it's fast and accurate. I also used OpenCV to handle the image preprocessing before sending it to the model.

## Tech Stack
- Python / Flask
- TensorFlow / Keras (MobileNetV2)
- OpenCV
- SQLite (for saving the prediction history)
- HTML, CSS, JavaScript

## How to run it locally

1. Clone this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```
   python app.py
   ```
4. Open your browser and go to `http://localhost:5000`

## Features
- Upload product images through a web interface.
- Uses OpenCV to resize and convert image colors.
- Predicts the item using a Convolutional Neural Network.
- Shows a confidence score for the prediction.
- Saves past predictions in an SQLite database so you can view them on the dashboard page.
