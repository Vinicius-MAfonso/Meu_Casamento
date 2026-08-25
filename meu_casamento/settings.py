from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import sys
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

env_file = BASE_DIR / ('.env.local' if os.getenv("DJANGO_ENV") != "production" else '.env.prod')
load_dotenv(env_file)

SECRET_KEY = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    if os.getenv("DJANGO_ENV") == "production":
        raise ImproperlyConfigured("SECRET_KEY must be configured in production.")
    SECRET_KEY = "django-insecure-test-secret-key-1234567890-abcdefghij"

DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]

# Automatically allow Cloud Run domains and custom wedding domains
for domain in [".run.app", ".a.run.app", ".rvwedding.com.br", "rvwedding.com.br"]:
    if domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(domain)

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

CSRF_TRUSTED_ORIGINS = [
    "https://*.run.app",
    "https://*.a.run.app",
    "https://rvwedding.com.br",
    "https://www.rvwedding.com.br",
]

# -------------------------
# Database configuration
# -------------------------

DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL.startswith("sqlite"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': DATABASE_URL.split(":///")[1],
        }
    }
elif DATABASE_URL != "":
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

RUNNING_TESTS = 'test' in sys.argv
if RUNNING_TESTS:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
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
    'csp',
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

if not DEBUG:
    MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
    MIDDLEWARE.insert(2, "csp.middleware.CSPMiddleware")

if DEBUG:
    MIDDLEWARE += ["django_browser_reload.middleware.BrowserReloadMiddleware"]

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if not DEBUG and not RUNNING_TESTS
        else "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

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
                'meu_casamento.context_processors.wedding_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'meu_casamento.wsgi.application'

# -------------------------
# Cache configuration
# -------------------------

def get_cache_settings(running_tests=False, django_env=None, cache_backend=None):
    django_env = (django_env or os.getenv("DJANGO_ENV", "")).lower()
    cache_backend = (cache_backend or os.getenv("CACHE_BACKEND", "")).strip().lower()

    if running_tests:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'meu-casamento-test-cache',
            }
        }

    if cache_backend == 'database':
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'django_cache_table',
            }
        }

    if cache_backend in {'locmem', 'memory', 'default'}:
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
                'LOCATION': 'meu-casamento-cache',
            }
        }

    if django_env == 'production':
        return {
            'default': {
                'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
                'LOCATION': 'django_cache_table',
            }
        }

    return {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'meu-casamento-cache',
        }
    }


CACHES = get_cache_settings(RUNNING_TESTS, os.getenv("DJANGO_ENV"), os.getenv("CACHE_BACKEND"))

# -------------------------
# Security settings
# -------------------------

if not DEBUG and not RUNNING_TESTS:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
    CONTENT_SECURITY_POLICY = {
        "DIRECTIVES": {
            "default-src": ["'self'"],
            "script-src": [
                "'self'",
                "cdnjs.cloudflare.com", "unpkg.com", "cdn.jsdelivr.net",
            ],
            "style-src": [
                "'self'", "'unsafe-inline'",
                "cdnjs.cloudflare.com", "unpkg.com", "fonts.googleapis.com",
            ],
            "font-src": ["'self'", "fonts.gstatic.com", "cdnjs.cloudflare.com"],
            "img-src": ["'self'", "data:"],
            "connect-src": ["'self'"],
        }
    }
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# -------------------------
# Internationalization
# -------------------------

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# -------------------------
# Wedding configuration
# -------------------------

WEDDING_DATE = '2026-11-22T10:00:00'

# RSVPs stop being accepted this many days before the wedding.
RSVP_CLOSE_DAYS_BEFORE = 30

# -------------------------
# Static files
# -------------------------

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tailwind
TAILWIND_APP_NAME = 'theme'

INTERNAL_IPS = ["127.0.0.1"]

# -------------------------
# Logging configuration
# -------------------------

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

if DEBUG and os.getenv("LOG_TO_FILE", "false").lower() == "true":
    LOGS_DIR = BASE_DIR / 'logs'
    LOGS_DIR.mkdir(exist_ok=True)
    LOGGING['handlers']['file'] = {
        'level': 'INFO',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': str(LOGS_DIR / 'django.log'),
        'maxBytes': 1024 * 1024 * 15,
        'backupCount': 10,
        'formatter': 'verbose',
    }
    LOGGING['loggers']['django']['handlers'].append('file')
    LOGGING['loggers']['core']['handlers'].append('file')

