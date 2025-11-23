#!/bin/bash

# Ensure environment variables are loaded
echo "Environment variables:"
echo "DEBUG=$DEBUG"
echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Making user admin..."
python make_admin.py

echo "Admin script completed"
echo "Starting server..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT