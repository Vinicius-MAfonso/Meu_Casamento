from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
env_file = BASE_DIR / ('.env.local' if os.getenv("DJANGO_ENV") != "production" else '.env.prod')
load_dotenv(env_file)

# Secret key
SECRET_KEY = os.getenv("SECRET_KEY")

# Debug mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Allowed hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

# -------------------------
# Database configuration
# -------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL.startswith("sqlite"):
    # Example: sqlite:///db.sqlite3
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATABASE_URL.split(":///")[1],
        }
    }
elif DATABASE_URL != "":
    # PostgreSQL, MySQL, etc.
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
    }
else:
    # Fallback for development without env var
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# -------------------------
# Apps
# -------------------------

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'theme',
    'core'
]

if DEBUG:
    INSTALLED_APPS += ["django_browser_reload"]

# -------------------------
# Middleware
# -------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Whitenoise for Render (production)
if not DEBUG:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

if DEBUG:
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

# -------------------------
# Templates
# -------------------------

ROOT_URLCONF = 'meu_casamento.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'meu_casamento.wsgi.application'

# -------------------------
# i18n
# -------------------------

LANGUAGE_CODE = 'pt-br'
TIMEZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# -------------------------
# Static files
# -------------------------

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "theme" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tailwind
TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ["127.0.0.1"]
