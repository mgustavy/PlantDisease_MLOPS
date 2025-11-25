FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Install tensorflow-cpu for smaller image size if possible, but for now stick to requirements or explicit
# optimizing for M1 macs locally vs linux container:
# The requirements.txt might have tensorflow-macos which won't work in linux container.
# We should use standard tensorflow for the container.
RUN pip install tensorflow

# Copy source code
COPY . .

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Script to run both
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
