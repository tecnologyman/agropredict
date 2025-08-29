from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Seguridad / Debug ──────────────────────────────────────────────────────────
# En local DEBUG=True. En Railway lo forzamos a False (si hay env var RAILWAY_*)
DEBUG = not bool(os.getenv("RAILWAY_ENVIRONMENT"))
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key-agropredict")

# Dominios permitidos
ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "agropredict.tecnologyman.cl",
]

# Si Railway expone dominio público, lo agregamos
RAILWAY_PUBLIC = os.getenv("RAILWAY_PUBLIC_DOMAIN") or os.getenv("RAILWAY_STATIC_URL")
if RAILWAY_PUBLIC:
    # Puede venir con o sin protocolo; normalizamos host
    host = RAILWAY_PUBLIC.replace("https://", "").replace("http://", "").strip("/")
    if host:
        ALLOWED_HOSTS.append(host)

# ── Apps ───────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise para archivos estáticos en producción
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "agropredict_project.urls"

# ── Templates ─────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "agropredict_project.wsgi.application"

# ── Base de datos (SQLite) ────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ── Password validators ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ── Internacionalización ──────────────────────────────────────────────────────
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# ── Archivos estáticos ────────────────────────────────────────────────────────
STATIC_URL = "/static/"
# Directorio de tus assets en el repo
STATICFILES_DIRS = [BASE_DIR / "static"]
# Destino de collectstatic (requerido en Railway/producción)
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise: sirve estáticos comprimidos y con manifest en producción
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ── Auto field ────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ── Login redirects ───────────────────────────────────────────────────────────
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
LOGIN_URL = "/accounts/login/"

# ── Seguridad detrás de proxy (Railway usa HTTPS) ─────────────────────────────
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ── CSRF Trust (tu dominio + Railway) ─────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    "https://agropredict.tecnologyman.cl",
    "https://*.up.railway.app",
]
if RAILWAY_PUBLIC:
    origin = RAILWAY_PUBLIC
    if not origin.startswith("http"):
        origin = "https://" + origin
    CSRF_TRUSTED_ORIGINS.append(origin.rstrip("/"))
