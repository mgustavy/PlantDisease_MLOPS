# Plant Disease Detection MLOps Pipeline

## Project Description
This project demonstrates an end-to-end Machine Learning pipeline for classifying plant diseases (Healthy, Powdery, Rust). It includes:
- **Data Processing**: Image resizing and normalization.
- **Model Training**: Transfer learning using MobileNetV2.
- **API**: FastAPI backend for predictions and retraining.
- **UI**: Streamlit frontend for easy interaction.
- **Deployment**: Dockerized for cloud deployment.
- **Monitoring**: Locust for load testing.

## Setup Instructions

### Prerequisites
- Docker installed
- Python 3.9+ installed

### Local Setup
1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd PlantDisease_MLOPS
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application (Manual)**
   - Backend: `uvicorn app:app --reload`
   - Frontend: `streamlit run frontend.py`

### Docker Setup (Recommended)
1. **Build the Image**
   ```bash
   docker build -t plant-disease-app .
   ```

2. **Run the Container**
   ```bash
   docker run -p 8000:8000 -p 8501:8501 plant-disease-app
   ```
   - Access UI at `http://localhost:8501`
   - Access API Docs at `http://localhost:8000/docs`

## Flood Request Simulation (Locust)
To simulate high traffic:
1. Install locust: `pip install locust`
2. Run locust: `locust -f locustfile.py`
3. Open `http://localhost:8089` and start the swarm.

## Video Demo
[Link to YouTube Demo]

## Directory Structure
```
Project_name/
│
├── README.md
├── Dockerfile
├── requirements.txt
├── locustfile.py
├── app.py
├── frontend.py
│
├── notebook/
│   └── plant_disease_pipeline.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── model.py
│   └── prediction.py
│
├── data/
│   ├── train/
│   └── Validation/
└── models/
   └── plant_disease_model.h5
```