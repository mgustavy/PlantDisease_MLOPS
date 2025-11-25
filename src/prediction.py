import tensorflow as tf
import numpy as np
from src.preprocessing import load_and_preprocess_single_image

def predict(model, image_path, class_names):
    """
    Predicts the class of an image using the loaded model.
    
    Args:
        model: The loaded Keras model.
        image_path: Path to the image file.
        class_names: List of class names corresponding to model outputs.
        
    Returns:
        dict: A dictionary containing the predicted class and confidence.
    """
    # Preprocess the image
    img_tensor = load_and_preprocess_single_image(image_path)
    
    # Make prediction
    predictions = model.predict(img_tensor)
    predicted_index = np.argmax(predictions[0])
    confidence = float(np.max(predictions[0]))
    
    return {
        "class": class_names[predicted_index],
        "confidence": confidence
    }
