FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -u 1000 -m appuser && \
    chown -R appuser:appuser /app

# Copy application
COPY . .

# Make start script executable
RUN chmod +x start.sh && \
    chown appuser:appuser start.sh

USER appuser

EXPOSE 8000