<<<<<<< HEAD
# MUSH - MushGuard Web Application

A Django web application for mushroom identification and classification.

## Deployment Ready for Render

This application is configured for production deployment on Render with:
- Production dependencies (gunicorn, whitenoise, psycopg2)
- Environment variable configuration
- PostgreSQL database support
- Static file handling with WhiteNoise
- Security best practices

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Render Deployment

The app includes `render.yaml` and `build.sh` for automatic deployment on Render platform.
=======
# Mushguard
web app
>>>>>>> ba805258c9405d2e93fb0c1995335a7e8d796f57
