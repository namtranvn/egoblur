#!/bin/bash
set -e

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Default number of workers based on CPU cores if not set
if [ -z "${WEB_CONCURRENCY}" ]; then
    export WEB_CONCURRENCY=$((2 * $(nproc) + 1))
fi

# Start Gunicorn
exec gunicorn main:app \
    --config gunicorn_conf.py \
    --workers ${WEB_CONCURRENCY} \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --log-level ${LOG_LEVEL:-info} \
    --timeout 120 \
    --keep-alive 120 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --access-logfile /app/logs/api_access.log \
    --error-logfile /app/logs/api.log