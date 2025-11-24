#!/bin/bash

# Ensure environment variables are loaded
echo "Environment variables:"
echo "DEBUG=$DEBUG"
echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"

# Only run migrations on first deploy (check if database exists)
if [ "$FIRST_DEPLOY" = "true" ]; then
    echo "Running migrations for first deploy..."
    python manage.py migrate --noinput
fi

echo "Making user admin..."
python make_admin.py

echo "Admin script completed"
echo "Starting server..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT