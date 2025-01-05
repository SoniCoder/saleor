#!/bin/bash
set -e

# Collect static files
echo "Collecting static files..."
SECRET_KEY=dummy STATIC_URL=${STATIC_URL:-/static/} python3 manage.py collectstatic --no-input

# Run the server
echo "Starting the server..."
gunicorn --bind :8000 --config gunicorn_config.py --reload --workers 4 --worker-class saleor.asgi.gunicorn_worker.UvicornWorker saleor.asgi:application