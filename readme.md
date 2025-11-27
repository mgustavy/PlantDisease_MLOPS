# PlantGuard AI

Welcome to **PlantGuard**, a smart tool designed to help identify plant diseases just by looking at a leaf.

🚀 **Live Demo:** [https://plant-disease-app-fme5.onrender.com/](https://plant-disease-app-fme5.onrender.com/)
**Video Demo:** [Video Demo](https://www.bugufi.link/X-3ufG)

## What is this?
I built this project to explore how we can use Machine Learning in a real-world application. The idea is simple: you upload a photo of a plant leaf, and the system tells you if it's healthy or if it has a disease like **Powdery Mildew** or **Rust**.

It's not just a model running in a notebook; it's a full pipeline that includes:
- A **FastAPI** backend that handles the logic.
- A **Streamlit** frontend that makes it easy to use.
- **Docker** support so it can run anywhere.
- **Locust** for testing how it handles traffic.

## How to Run It
You can play with the live demo above, but if you want to run it on your own machine, here's how:

### The Easy Way (Docker)
If you have Docker installed, you can get it up and running with just two commands:

1.  **Build the app:**
    ```bash
    docker build -t plant-disease-app .
    ```
2.  **Run it:**
    ```bash
    docker run -p 8501:8501 plant-disease-app
    ```
    Then just open `http://localhost:8501` in your browser.

### The Manual Way
If you prefer running it with Python directly:

1.  **Install the requirements:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Start the app:**
    ```bash
    ./start.sh
    ```

## Project Structure
Here's a quick look at how I organized the code:

- `app.py`: The brain of the operation (API).
- `frontend.py`: The user interface you see.
- `notebook/`: Where I experimented and trained the model.
- `src/`: Helper scripts for processing images and making predictions.
- `Dockerfile`: Where the packaging the app is handled.

## Tech Stack
- **Python** (of course!)
- **TensorFlow/Keras** for the AI model.
- **FastAPI** for the backend.
- **Streamlit** for the UI.
- **Render** for hosting.
