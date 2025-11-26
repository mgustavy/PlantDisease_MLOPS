#!/bin/bash
uvicorn app:app --host 0.0.0.0 --port 8000 &
# Default to port 8501 if PORT is not set
PORT="${PORT:-8501}"
streamlit run frontend.py --server.port $PORT --server.address 0.0.0.0
