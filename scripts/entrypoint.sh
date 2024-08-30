#!/bin/sh

# Load environment variables from .env file
export $(grep -v '^#' /backend/.env | xargs)

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Define the number of workers and threads
# Based on the number of CPU cores
# Formula: 2 * (number of CPU cores) + 1

WORKERS=${GUNICORN_WORKERS:-3}
THREADS=${GUNICORN_THREADS:-2}

gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers "$WORKERS" --threads "$THREADS"
