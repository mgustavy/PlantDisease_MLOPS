# src/preprocessing.py

def normalize_and_resize(image):
    """Resizes and scales image pixel values to [0, 1]."""
    # Resize the image (e.g., to 224x224) if it's not already
    image = tf.image.resize(image, [224, 224])
    # Scale pixel values from 0-255 to 0-1
    return image / 255.0

def load_and_preprocess_single_image(image_path, target_size=(224, 224)):
    """Loads a single image from a path and applies preprocessing."""
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3) # Assuming JPEGs
    img = normalize_and_resize(img)
    # Add a batch dimension for the model
    return tf.expand_dims(img, axis=0)