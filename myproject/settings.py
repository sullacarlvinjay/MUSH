"""
Django settings for myproject project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured('SECRET_KEY environment variable is required in production')
    SECRET_KEY = 'django-insecure-local-development-only'

ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Render sets this to the service's public hostname (e.g. mushguard.onrender.com)
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    f'https://*{h}' if h.startswith('.') else f'https://{h}'
    for h in ALLOWED_HOSTS if h not in ('localhost', '127.0.0.1')
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

# Database: Supabase Postgres when DATABASE_URL is set, SQLite otherwise.
# On Render use Supabase's *Session pooler* connection string (IPv4); the
# direct db.<ref>.supabase.co host is IPv6-only.
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not DEBUG,
        )
    }
elif not DEBUG:
    raise ImproperlyConfigured('DATABASE_URL environment variable is required in production')
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# User uploads: Supabase Storage (S3-compatible API) when configured, local
# disk otherwise. Render's disk is wiped on every deploy, so production
# needs Supabase Storage.
SUPABASE_PROJECT_REF = os.getenv('SUPABASE_PROJECT_REF')
SUPABASE_STORAGE_BUCKET = os.getenv('SUPABASE_STORAGE_BUCKET', 'media')
USE_SUPABASE_STORAGE = bool(SUPABASE_PROJECT_REF and os.getenv('SUPABASE_S3_ACCESS_KEY_ID'))

if USE_SUPABASE_STORAGE:
    DEFAULT_STORAGE = {
        'BACKEND': 'storages.backends.s3.S3Storage',
        'OPTIONS': {
            'bucket_name': SUPABASE_STORAGE_BUCKET,
            'endpoint_url': f'https://{SUPABASE_PROJECT_REF}.storage.supabase.co/storage/v1/s3',
            'region_name': os.getenv('SUPABASE_S3_REGION', 'ap-southeast-1'),
            'access_key': os.getenv('SUPABASE_S3_ACCESS_KEY_ID'),
            'secret_key': os.getenv('SUPABASE_S3_SECRET_ACCESS_KEY'),
            # Bucket is public: serve plain public URLs instead of signed ones
            'custom_domain': f'{SUPABASE_PROJECT_REF}.supabase.co/storage/v1/object/public/{SUPABASE_STORAGE_BUCKET}',
            'querystring_auth': False,
            'default_acl': None,
            'file_overwrite': False,
            'addressing_style': 'path',
            'signature_version': 's3v4',
        },
    }
else:
    if not DEBUG:
        print('WARNING: Supabase Storage is not configured; uploads will be lost on redeploy')
    DEFAULT_STORAGE = {'BACKEND': 'django.core.files.storage.FileSystemStorage'}

STORAGES = {
    'default': DEFAULT_STORAGE,
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage'},
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# HTTPS (Render terminates TLS at its proxy)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '3600'))
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = 'same-origin'

# Email: Brevo API with console fallback
EMAIL_BACKEND = 'core.email_backends.BrevoEmailBackend'
BREVO_API_KEY = os.getenv('BREVO_API_KEY', '')
BREVO_SENDER_EMAIL = os.getenv('BREVO_SENDER_EMAIL', '')  # must be verified in Brevo
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', f'MushGuard <{BREVO_SENDER_EMAIL}>')
EMAIL_SUBJECT_PREFIX = '[MushGuard] '

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': os.getenv('LOG_LEVEL', 'INFO')},
}
