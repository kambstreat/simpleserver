# app.py
# This is the main application file for your Flask server.

from flask import Flask, request, jsonify
from PIL import Image # Pillow library for image processing
import io # Used to handle image bytes in memory
import os # To access environment variables like PORT

# Initialize the Flask application
app = Flask(__name__)

# --- Dummy ML Model Function ---
# In a real application, you would load and use a trained machine learning model here.
# For this prototype, we'll perform a simple image analysis to demonstrate the flow.
def run_ml_model(image_bytes):
    """
    Simulates an ML model that takes raw image bytes and returns a prediction.
    This example checks if the image is grayscale or color.
    """
    try:
        # Open the image from bytes using Pillow
        image = Image.open(io.BytesIO(image_bytes))

        # Get image dimensions
        width, height = image.size

        # Perform a simple "prediction" based on image properties
        prediction = "Unknown Image Type"
        if image.mode == 'L': # 'L' mode typically means grayscale
            prediction = "Grayscale Image Detected"
        elif image.mode in ('RGB', 'RGBA'): # 'RGB' or 'RGBA' for color images
            prediction = "Color Image Detected"

        # You would replace this with actual ML model inference, e.g.:
        # from your_ml_library import YourModel
        # model = YourModel.load('path/to/your/model.h5')
        # processed_image = preprocess_image_for_model(image)
        # ml_output = model.predict(processed_image)
        # prediction = interpret_ml_output(ml_output)

        return {
            "prediction": prediction,
            "image_size": f"{width}x{height}",
            "image_mode": image.mode,
            "message": "This is a prototype prediction. Replace with a real ML model!"
        }

    except Exception as e:
        # Handle potential errors during image processing
        return {"error": f"Error processing image: {str(e)}"}

# --- API Endpoint for ML Prediction ---
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handles POST requests to the /predict endpoint.
    Expects an image file in the request.
    """
    # Check if an 'image' file was sent in the request
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided in the request."}), 400

    image_file = request.files['image']

    # Check if the file name is empty (no file selected)
    if image_file.filename == '':
        return jsonify({"error": "No selected image file."}), 400

    # If an image file is present and has a filename
    if image_file:
        try:
            # Read the image file into bytes
            image_bytes = image_file.read()
            # Pass the image bytes to our dummy ML model
            # return the same image in Grey
            image_bytes = Image.open(io.BytesIO(image_bytes)).convert('L')

            #result = run_ml_model(image_bytes)
            # how to return image_bytes as a response
            img_byte_arr = io.BytesIO()
            image_bytes.save(img_byte_arr, format='PNG')  # Save as PNG or any other format
            img_byte_arr.seek(0)  # Move to the beginning of the Bytes
            image_bytes = img_byte_arr.getvalue()  # Get the byte data
            # Return the processed image bytes as a response
            # Set the content type to image/png or image/jpeg as appropriate
            #return jsonify({"message": "Image processed successfully", "image_bytes": image_bytes}), 200
            return image_bytes, 200, {'Content-Type': 'image/png'}

        except Exception as e:
            # Catch any errors during file reading or model execution
            return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
    else:
        # This case should ideally be caught by the above checks, but included for robustness
        return jsonify({"error": "An unexpected error occurred with the image file."}), 500

# --- Home Route ---
@app.route('/')
def home():
    """
    A simple home route to confirm the server is running.
    """
    return "<h1>ML Prototype Server is Running!</h1><p>Send a POST request to <code>/predict</code> with an image file.</p>"

# --- Server Start ---
if __name__ == '__main__':
    # Render will automatically set the PORT environment variable.
    # We use os.getenv to get it, defaulting to 5000 for local development.
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
