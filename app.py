import uvicorn
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import shutil
import os
from src.model import load_model, train_model, create_compiled_model
from src.prediction import predict
from src.preprocessing import load_and_preprocess_single_image
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

app = FastAPI(title="Plant Disease Classification API")

# Global variables
MODEL_PATH = "models/plant_disease_model.h5"
DATA_DIR = "data"
CLASS_NAMES = ["Healthy", "Powdery", "Rust"]

# Load model on startup
try:
    model = load_model(MODEL_PATH)
    print("Model loaded successfully.")
except:
    print("Model not found. Please retrain.")
    model = None

@app.get("/")
def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict_endpoint(file: UploadFile = File(...)):
    if model is None:
        return JSONResponse(status_code=503, content={"error": "Model not loaded"})
    
    # Save temp file
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        result = predict(model, temp_filename, CLASS_NAMES)
        return result
    finally:
        os.remove(temp_filename)

def retrain_model_task():
    global model
    print("Starting retraining...")
    # Load data
    train_datagen = ImageDataGenerator(rescale=1./255)
    train_generator = train_datagen.flow_from_directory(
        f"{DATA_DIR}/train",
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )
    
    # Create and train new model
    new_model = create_compiled_model(input_shape=(224, 224, 3), num_classes=len(CLASS_NAMES))
    train_model(new_model, train_generator, epochs=5) # Reduced epochs for demo
    
    # Save and update global model
    new_model.save(MODEL_PATH)
    model = new_model
    print("Retraining complete and model updated.")

@app.post("/retrain")
async def retrain_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(retrain_model_task)
    return {"message": "Retraining started in background"}

@app.post("/upload")
async def upload_data(file: UploadFile = File(...), label: str = "Healthy"):
    # Save uploaded file to training data
    target_dir = f"{DATA_DIR}/train/{label}"
    os.makedirs(target_dir, exist_ok=True)
    
    file_path = f"{target_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"message": f"File saved to {target_dir}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
