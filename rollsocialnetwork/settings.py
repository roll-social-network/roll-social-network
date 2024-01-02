"""
roll social network settings.
"""

from pathlib import Path
from typing import List
from decouple import config  # type: ignore[import-untyped]
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-q=u8&7w8!%khn7a$lj5drzm9i)k90fh7m_-0b14pjxfz51d(ah"
)
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS: List[str] = []
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "phonenumber_field",
    "rollsocialnetwork.phone_auth",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
]
ROOT_URLCONF = "rollsocialnetwork.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            "./rollsocialnetwork/templates",
            "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "rollsocialnetwork.context_processors.is_home_site"
            ],
        },
    },
]
WSGI_APPLICATION = "rollsocialnetwork.wsgi.application"
DATABASES = {
    "default": dj_database_url.parse(config("DATABASES_DEFAULT", default="sqlite:///./db.sqlite3"))
}
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "rollsocialnetwork.phone_auth.backends.PhoneAuthBackend",
]
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/phoneauth/request/"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATICFILES_DIRS = [
    "roll-social-network-frontend/dist",
]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = config("SITE_ID", default=None, cast=lambda v: None if v is None else int(v))
HOME_SITE_ID = config("HOME_SITE_ID", default=1, cast=int)
PHONE_AUTH_VALIDATION_CODE_TTL = config("PHONE_AUTH_VALIDATION_CODE_TTL", default=60, cast=int)
PHONE_AUTH_VALIDATION_CODE_LENGTH = config("PHONE_AUTH_VALIDATION_CODE_LENGTH", default=4, cast=int)
PHONE_AUTH_VERIFY_ATTEMPTS = config("PHONE_AUTH_VERIFY_ATTEMPTS", default=3, cast=int)
PHONE_AUTH_SMS_GATEWAY = config("PHONE_AUTH_SMS_GATEWAY", default="logger")
PHONE_AUTH_SMS_GATEWAY_ARGS = config("PHONE_AUTH_SMS_GATEWAY_ARGS", default="", cast=str.split)
