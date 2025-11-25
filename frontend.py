import streamlit as st
import requests
from PIL import Image
import os

st.set_page_config(page_title="Plant Disease Classifier", layout="wide")

API_URL = "http://localhost:8000"

st.title("Plant Disease Classification System")

# Sidebar for navigation
page = st.sidebar.selectbox("Navigate", ["Prediction", "Dashboard", "Admin"])

if page == "Prediction":
    st.header("Upload an Image for Prediction")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        if st.button("Predict"):
            files = {"file": uploaded_file.getvalue()}
            try:
                response = requests.post(f"{API_URL}/predict", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Prediction: **{result['class']}**")
                    st.info(f"Confidence: {result['confidence']:.2f}")
                else:
                    st.error("Error getting prediction. Is the backend running?")
            except Exception as e:
                st.error(f"Connection error: {e}")

elif page == "Dashboard":
    st.header("Data Visualization")
    
    # Simple visualization of class distribution
    data_dir = "data/train"
    if os.path.exists(data_dir):
        classes = os.listdir(data_dir)
        classes = [c for c in classes if not c.startswith('.')]
        counts = {}
        for c in classes:
            counts[c] = len(os.listdir(os.path.join(data_dir, c)))
            
        st.bar_chart(counts)
        st.caption("Number of training images per class")
    else:
        st.warning("Data directory not found.")

elif page == "Admin":
    st.header("System Administration")
    
    # Health Check
    try:
        health = requests.get(f"{API_URL}/").json()
        st.write("System Status:", health)
    except:
        st.error("Backend is offline.")
        
    st.divider()
    
    # Retrain
    st.subheader("Retrain Model")
    if st.button("Trigger Retraining"):
        try:
            res = requests.post(f"{API_URL}/retrain")
            st.success(res.json()["message"])
        except:
            st.error("Failed to trigger retraining.")
            
    st.divider()
    
    # Bulk Upload
    st.subheader("Upload Training Data")
    upload_files = st.file_uploader("Upload images", accept_multiple_files=True)
    label = st.selectbox("Select Class", ["Healthy", "Powdery", "Rust"])
    
    if st.button("Upload Data") and upload_files:
        progress_bar = st.progress(0)
        for i, file in enumerate(upload_files):
            files = {"file": file.getvalue()}
            requests.post(f"{API_URL}/upload", params={"label": label}, files=files)
            progress_bar.progress((i + 1) / len(upload_files))
        st.success("Upload complete!")
