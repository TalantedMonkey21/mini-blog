from pathlib import Path
import os
from dotenv import load_dotenv

# --- БАЗОВЫЕ НАСТРОЙКИ --------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Подгрузим .env (если есть локально)
load_dotenv()

# Секрет и debug из окружения
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "change-me-in-env")
DEBUG = os.getenv("DJANGO_DEBUG", "0").lower() in ("1", "true", "yes", "on")

# ALLOWED_HOSTS:
# если DJANGO_ALLOWED_HOSTS="*", то разрешаем всех; иначе парсим список через запятую.
_raw_hosts = os.getenv("DJANGO_ALLOWED_HOSTS", "*").strip()
if _raw_hosts == "*":
    ALLOWED_HOSTS = ["*"]
else:
    ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

# CSRF_TRUSTED_ORIGINS — только из окружения (при необходимости задайте там)
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# --- ПРИЛОЖЕНИЯ ---------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog",
    "rest_framework",
]

# --- MIDDLEWARE ---------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blog_project.urls"

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

WSGI_APPLICATION = "blog_project.wsgi.application"

# --- БАЗА ДАННЫХ --------------------------------------------------------------
# Если заданы POSTGRES_* — используем Postgres; иначе SQLite (для локалки)
if os.getenv("POSTGRES_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "blogdb"),
            "USER": os.getenv("POSTGRES_USER", "bloguser"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "blogpass"),
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# --- ПАРОЛИ -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- ЛОКАЛИЗАЦИЯ --------------------------------------------------------------
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

# --- СТАТИКА ------------------------------------------------------------------
STATIC_URL = "/static/"
# Куда collectstatic будет собирать файлы (важно для продакшена/K8s)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# WhiteNoise для раздачи статики из STATIC_ROOT
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- ПРОЧЕЕ -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGOUT_REDIRECT_URL = "/"
LOGIN_REDIRECT_URL = "/"