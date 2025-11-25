# src/model.py
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.applications import MobileNetV2 # Good balance of speed and accuracy

def create_compiled_model(input_shape, num_classes):
    """Defines and compiles a MobileNetV2-based Transfer Learning model."""

    # 1. Load Pre-trained Base Model
    # input_shape should match your resized image dimensions (e.g., 224, 224, 3)
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False, # We don't want their final classification layer
        weights='imagenet'
    )
    # Freeze the base layers so they don't lose their learned features during initial training
    base_model.trainable = False

    # 2. Build the Model Head (Custom Classifier)
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(), # Reduces feature map size for Dense layer
        Dropout(0.5),            # Regularization to prevent overfitting
        Dense(num_classes, activation='softmax') # Final classification layer
    ])

    # 3. Compile the Model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy', # Use for multi-class classification
        metrics=['accuracy']
    )
    
    return model

def train_model(model, train_data, epochs=10):
    """Trains the model and returns the history object."""
    print("Starting model training...")
    history = model.fit(
        train_data,
        epochs=epochs,
        # You would typically add a validation set here
    )
    print("Training complete.")
    return history