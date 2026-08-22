"""
Django settings for the Goat Farm website + admin panel + internal farm app.

Works two ways, automatically:
- LOCALLY (on your Windows machine): no environment variables needed —
  it falls back to SQLite, DEBUG=True, and local file storage, exactly
  like before. Nothing changes for your day-to-day workflow.
- IN PRODUCTION (e.g. on Render): set the environment variables listed
  below in the hosting dashboard, and it automatically switches to a real
  Postgres database, Cloudinary for media storage, and secure settings.
"""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Core security settings — read from environment in production, safe
# defaults for local development.
# ---------------------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-change-this-before-deploying-REPLACE-ME"
)

# DEBUG is True locally by default. On Render, set DEBUG=False as an
# environment variable.
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Add your real domain(s) here. RENDER_EXTERNAL_HOSTNAME is auto-provided
# by Render for the *.onrender.com URL; ALLOWED_HOSTS below adds your
# custom domain on top of that automatically once set as an env var.
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "simalthali-agro-private-limited.onrender.com",
]

extra_hosts = os.environ.get("ALLOWED_HOSTS", "")

if extra_hosts:
    ALLOWED_HOSTS += [
        h.strip()
        for h in extra_hosts.split(",")
        if h.strip()
    ]

render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME")

if render_hostname and render_hostname not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(render_hostname)

CSRF_TRUSTED_ORIGINS = [
    f"https://{h}"
    for h in ALLOWED_HOSTS
    if h not in ("localhost", "127.0.0.1")
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    "cloudinary",
    "core",  # our website app
    "farmapp",  # internal tracking app (health, milk, breeding, feed)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serves static files in production
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "goat_farm.urls"

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

WSGI_APPLICATION = "goat_farm.wsgi.application"

# ---------------------------------------------------------------------------
# Database — SQLite locally, Postgres in production (via DATABASE_URL).
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

database_url = os.environ.get("DATABASE_URL")
if database_url:
    DATABASES["default"] = dj_database_url.parse(database_url, conn_max_age=600)

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static files — served efficiently in production by WhiteNoise.
# # ---------------------------------------------------------------------------
# STATIC_URL = "static/"
# STATICFILES_DIRS = [BASE_DIR / "core" / "static"]
# STATIC_ROOT = BASE_DIR / "staticfiles"
# STORAGES = {
#     "staticfiles": {
#         "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#     },
# }

# # ---------------------------------------------------------------------------
# # Media files (goat photos, product images, etc.) — local disk in
# # development, Cloudinary in production (set CLOUDINARY_URL to enable).
# # Without this, uploaded photos would be permanently lost every time
# # Render restarts or redeploys the app, since its free disk is temporary.
# # ---------------------------------------------------------------------------
# MEDIA_URL = "media/"
# MEDIA_ROOT = BASE_DIR / "media"

# if os.environ.get("CLOUDINARY_URL"):
#     STORAGES["default"] = {"BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage"}






STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

if os.environ.get("CLOUDINARY_URL"):
    STORAGES["default"] = {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    }













# ---------------------------------------------------------------------------
# Production security hardening — only applied when DEBUG is False.
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
