#!/bin/bash

trap "echo 'Stopping all services...'; kill 0" EXIT

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Starting Redis..."
docker start redis 2>/dev/null || docker run -d --name redis -p 6379:6379 redis

echo "Starting Celery..."
celery -A config worker --loglevel=info &

echo "Starting Django server..."
uv run python manage.py runserver
