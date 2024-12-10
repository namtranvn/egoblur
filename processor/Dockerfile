FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies including FFmpeg
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git \
    ffmpeg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -u 1000 -m appuser

RUN chown -R appuser:appuser /app

COPY . .

USER appuser
