#!/bin/bash
set -e

# Create logs directory if it doesn't exist
mkdir -p /app/logs

# Start Celery with logging
exec celery -A tasks worker -c 3\
    --loglevel=info \
    --logfile=/app/logs/celery.log

# exec celery -A tasks worker -P eventlet -c 3 --loglevel=info --logfile=/app/logs/celery.log

# exec celery -A tasks worker -P solo --loglevel=info --logfile=/app/logs/celery.log