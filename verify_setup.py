import os
import tensorflow as tf
import numpy as np
from src.model import create_compiled_model, save_model, load_model
from src.prediction import predict
from src.preprocessing import normalize_and_resize

def verify_pipeline():
    print("Verifying pipeline...")
    
    # 1. Verify Model Creation
    print("Creating model...")
    model = create_compiled_model((224, 224, 3), 3)
    assert model is not None
    print("Model created.")
    
    # 2. Verify Model Saving/Loading
    print("Saving model...")
    os.makedirs("models", exist_ok=True)
    save_path = "models/test_model.h5"
    save_model(model, save_path)
    assert os.path.exists(save_path)
    print("Model saved.")
    
    print("Loading model...")
    loaded_model = load_model(save_path)
    assert loaded_model is not None
    print("Model loaded.")
    
    # 3. Verify Preprocessing
    print("Verifying preprocessing...")
    dummy_image = tf.zeros((300, 300, 3))
    processed_image = normalize_and_resize(dummy_image)
    assert processed_image.shape == (224, 224, 3)
    print("Preprocessing working.")
    
    # 4. Verify Prediction (Mock)
    # We can't easily mock the file reading part of predict() without a real file
    # But we can verify the model prediction on a tensor
    print("Verifying model inference...")
    dummy_input = tf.expand_dims(processed_image, axis=0)
    prediction = loaded_model.predict(dummy_input)
    assert prediction.shape == (1, 3)
    print("Inference working.")
    
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    verify_pipeline()
