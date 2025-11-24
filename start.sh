#!/bin/bash

# Ensure environment variables are loaded
echo "Environment variables:"
echo "DEBUG=$DEBUG"
echo "ALLOWED_HOSTS=$ALLOWED_HOSTS"

# NEVER run migrations on startup - they corrupt the database
echo "Skipping migrations - database should already be set up"

# Only create admin if no users exist (prevents recreation)
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from django.contrib.auth.models import User
if User.objects.count() == 0:
    print('Creating admin user...')
    User.objects.create_superuser('admin', 'admin@mushguard.com', 'admin123')
else:
    print('Users already exist, skipping admin creation')
"

echo "Starting server..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT