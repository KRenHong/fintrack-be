"""
Base settings for the Django backend (shared by dev & prod).
"""
from __future__ import annotations

from pathlib import Path
import os
import environ
from datetime import timedelta

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /config/settings/../..

# ---------------------------------------------------------
# Env
# ---------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ""),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CORS_ALLOWED_ORIGINS=(list, []),
    CSRF_TRUSTED_ORIGINS=(list, []),
    TIME_ZONE=(str, "Asia/Kuala_Lumpur"),
)
# Read .env if present
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY") or ("dev-secret-key" if DEBUG else "")
if not SECRET_KEY and not DEBUG:
    raise RuntimeError("SECRET_KEY must be set in production")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# ---------------------------------------------------------
# Installed apps
# ---------------------------------------------------------
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # 3rd-party
    "rest_framework",
    "django_filters",
    "corsheaders",
    "djoser",
    "django_extensions",

    # Local apps
    "accounts",
    "transactions",
    "categories",
    "budgets",
]

# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------
# URLs / WSGI / ASGI
# ---------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
# (If you create ASGI later)
# ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Add template dirs if you serve server-rendered pages
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------
# Database (sqlite by default; switch to Postgres in prod)
# If you want DATABASE_URL support, uncomment and set in .env, e.g.:
# DATABASE_URL=postgres://user:pass@host:5432/dbname
# ---------------------------------------------------------
if env("DEBUG"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Default to sqlite if DATABASE_URL is not provided
    DATABASE_URL = os.getenv("DATABASE_URL")
    if DATABASE_URL:
        # Requires 'django-environ' which we already use
        DATABASES = {"default": env.db("DATABASE_URL")}
    else:
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }

# ---------------------------------------------------------
# Auth
# ---------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"

# ---------------------------------------------------------
# REST Framework / Filters / JWT
# ---------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

from rest_framework.settings import api_settings as _drf  # noqa: E402

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

DJOSER = {
    "LOGIN_FIELD": "username",  # set to 'email' if you prefer email login
    "USER_ID_FIELD": "id",
    "SERIALIZERS": {
        # Add custom serializers if you create them
        # "user_create": "accounts.serializers.RegisterSerializer",
        # "user": "accounts.serializers.ProfileSerializer",
    },
}

# ---------------------------------------------------------
# i18n / tz
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# Static / Media
# ---------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------
# CORS / CSRF for separate FE repo
# ---------------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# ---------------------------------------------------------
# Default primary key
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------
# Logging (simple console log; extend as needed)
# ---------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}
