# agropredict_project/settings.py
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Básico / Entorno ---
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-agropredict-styled')
DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'

# Por defecto incluye localhost y dominios típicos de despliegue temporal
ALLOWED_HOSTS = [
    '127.0.0.1', 'localhost',
    '.onrender.com', '.railway.app', '.fly.dev',
    "agropredict.tecnologyman.cl",
    "web-production-6662.up.railway.app",
    os.environ.get("RAILWAY_STATIC_URL", ""),
]
ALLOWED_HOSTS = [h for h in ALLOWED_HOSTS if h]  # limpia vacíos

# Si tu plataforma exige CSRF explícito (Render, Fly, etc.)
_csrf_env = os.getenv('DJANGO_CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [
    "https://agropredict.tecnologyman.cl",
    "https://web-production-6662.up.railway.app",
]
# Ejemplo de valor: https://tu-servicio.onrender.com,https://algo.railway.app

# --- Apps ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    # WhiteNoise: usar su servidor de estáticos (desactiva el de runserver)
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'core',
]

# --- Middleware ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise para archivos estáticos en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'agropredict_project.urls'

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

WSGI_APPLICATION = 'agropredict_project.wsgi.application'

# --- Base de datos (SQLite) ---
# Nota: en plataformas serverless/containers el disco puede ser efímero.
# Para demo temporal está OK; no recomendado para datos persistentes.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Permite sobreescribir por env si quieres (p. ej. /data/db.sqlite3)
        'NAME': os.getenv('SQLITE_NAME', BASE_DIR / 'db.sqlite3'),
    }
}

# --- Passwords ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Locale ---
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# --- Archivos estáticos ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # donde pones tus assets en desarrollo
STATIC_ROOT = BASE_DIR / 'staticfiles'    # colecta aquí para producción

# WhiteNoise storage con hash del archivo (cache busting)
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# --- Seguridad detrás de proxy (Render, Railway, etc.) ---
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Auth redirects ---
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
