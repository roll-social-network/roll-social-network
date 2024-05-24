"""
roll social network settings.
"""

import json
import os
from typing import Optional
from pathlib import Path
from decouple import config  # type: ignore[import-untyped]
import dj_database_url
import corsheaders.defaults

def oidc_rsa_private_key_cast(value: Optional[str]) -> Optional[str]:
    """
    oidc rsa private key cast
    """
    if not value:
        return None
    if os.path.isfile(value):
        return open(value, encoding="utf-8").read()
    return value

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config(
    "SECRET_KEY",
    default="django-insecure-q=u8&7w8!%khn7a$lj5drzm9i)k90fh7m_-0b14pjxfz51d(ah"
)
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=str.split)
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.humanize",
    "phonenumber_field",
    "easy_thumbnails",
    "corsheaders",
    "channels",
    "oauth2_provider",
    "social_django",
    "rest_framework",
    "rest_framework.authtoken",
    "rollsocialnetwork",
    "rollsocialnetwork.phone_auth",
    "rollsocialnetwork.social",
    "rollsocialnetwork.timeline",
    "rollsocialnetwork.oidc",
    "rollsocialnetwork.api",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "rollsocialnetwork.social.middleware.CurrentUserProfileMiddleware",
    "csp.middleware.CSPMiddleware",
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
                "rollsocialnetwork.context_processors.home_site",
                "rollsocialnetwork.context_processors.another_rolls",
                "rollsocialnetwork.social.context_processors.social",
                "rollsocialnetwork.phone_auth.context_processors.otp_secret_validated",
            ],
        },
    },
]
WSGI_APPLICATION = "rollsocialnetwork.wsgi.application"
ASGI_APPLICATION = "rollsocialnetwork.asgi.application"
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
ENABLE_OIDC = config("ENABLE_OIDC",default=False,
                               cast=bool)
AUTHENTICATION_BACKENDS = []
if ENABLE_OIDC:
    AUTHENTICATION_BACKENDS += [
        "rollsocialnetwork.oidc.backends.RollOpenIdConnectAuth",
    ]
AUTHENTICATION_BACKENDS += [
    "rollsocialnetwork.phone_auth.backends.PhoneAuthBackend",
    "rollsocialnetwork.phone_auth.backends.PhoneAuthOTPBackend",
    "django.contrib.auth.backends.ModelBackend",
]
LOGIN_REDIRECT_URL = "/t/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login/"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = config("STATIC_URL",
                    default="static/")
STATICFILES_DIRS = [
    "ui/dist",
    "rollsocialnetwork/static",
]
STATIC_ROOT = config("STATIC_ROOT",
                     default=None)
MEDIA_ROOT = config("MEDIA_ROOT", default="./media/")
MEDIA_URL = config("MEDIA_URL", default="/media/")
MEDIA_PATH_AS_STATIC = config("MEDIA_PATH_AS_STATIC",
                              default=False,
                              cast=bool)
MEDIA_PATH_AS_NGINX_ACCEL = config("MEDIA_PATH_AS_NGINX_ACCEL",
                                   default=False,
                                   cast=bool)
NGINX_ACCEL_REDIRECT_INTERNAL_LOCATION = config("NGINX_ACCEL_REDIRECT_INTERNAL_LOCATION",
                                                default="/medias/")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SITE_ID = config("SITE_ID", default=None, cast=lambda v: None if v is None else int(v))
HOME_SITE_ID = config("HOME_SITE_ID", default=1, cast=int)
PHONE_AUTH_VALIDATION_CODE_TTL = config("PHONE_AUTH_VALIDATION_CODE_TTL", default=60, cast=int)
PHONE_AUTH_VALIDATION_CODE_LENGTH = config("PHONE_AUTH_VALIDATION_CODE_LENGTH", default=4, cast=int)
PHONE_AUTH_VERIFY_ATTEMPTS = config("PHONE_AUTH_VERIFY_ATTEMPTS", default=3, cast=int)
PHONE_AUTH_SMS_GATEWAY = config("PHONE_AUTH_SMS_GATEWAY", default="logger")
PHONE_AUTH_SMS_GATEWAY_ARGS = config("PHONE_AUTH_SMS_GATEWAY_ARGS", default="", cast=str.split)
CREATE_USER_PROFILE_URL = "/s/create-user-profile/"
THUMBNAIL_ALIASES = {
    'timeline': {
        'photo8': {
            'size': (8, 8),
            'crop': True,
            'upscale': True,
            'quality': 10,
        },
        'photo184': {
            'size': (184, 184),
            'crop': True,
            'upscale': True,
            'quality': 50,
        },
        'photo584': {
            'size': (584, 584),
            'crop': True,
            'upscale': True,
            'quality': 90,
        },
    }
}
THUMBNAIL_DEFAULT_STORAGE = config("THUMBNAIL_DEFAULT_STORAGE",
                                   default="easy_thumbnails.storage.ThumbnailFileSystemStorage")
CORS_ALLOW_ALL_ORIGINS = config("CORS_ALLOW_ALL_ORIGINS",
                                default=False,
                                cast=bool)
CORS_ALLOWED_ORIGIN_REGEXES = config("CORS_ALLOWED_ORIGIN_REGEXES",
                                     default="",
                                     cast=lambda value: value.split(","))
CORS_ALLOW_HEADERS = [
    *corsheaders.defaults.default_headers,
    "action-component",
]
CORS_ALLOW_CREDENTIALS = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = "unsafe-none"
SESSION_COOKIE_DOMAIN = config("SESSION_COOKIE_DOMAIN",
                               default=None)
CSP_CONNECT_SRC = config("CSP_CONNECT_SRC",
                         default="'self'",
                         cast=lambda value: value.split(","))
CSP_SCRIPT_SRC = config("CSP_SCRIPT_SRC",
                        default="'self','unsafe-eval'",
                        cast=lambda value: value.split(","))
CSP_STYLE_SRC = config("CSP_STYLE_SRC",
                       default="'self','unsafe-hashes',fonts.googleapis.com",
                       cast=lambda value: value.split(","))
CSP_FONT_SRC = config("CSP_FONT_SRC",
                      default="'self',fonts.gstatic.com",
                      cast=lambda value: value.split(","))
CSP_IMG_SRC = config("CSP_IMG_SRC",
                     default="'self',data:",
                     cast=lambda value: value.split(","))
STORAGES = {
    "default": {
        "BACKEND": config("STORAGES_DEFAULT_BACKEND",
                          default="django.core.files.storage.FileSystemStorage"),
        "OPTIONS": config("STORAGES_DEFAULT_OPTIONS",
                          default="{}",
                          cast=json.loads)
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
    },
    "posts": {
        "BACKEND": config("STORAGES_POSTS_BACKEND",
                          default="django.core.files.storage.FileSystemStorage"),
        "OPTIONS": config("STORAGES_POSTS_OPTIONS",
                          default="{}",
                          cast=json.loads)
    }
}
FTP_STORAGE_LOCATION = config("FTP_STORAGE_LOCATION",
                              default=None)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": config("CHANNEL_LAYERS_DEFAULT_BACKEND",
                          default="channels.layers.InMemoryChannelLayer"),
        "CONFIG": config("CHANNEL_LAYERS_DEFAULT_CONFIG",
                         default="{}",
                         cast=json.loads)
    }
}
SUBDOMAIN_BASE = config("SUBDOMAIN_BASE",
                        default="roll.local")
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS",
                              default=f"https://{SUBDOMAIN_BASE},https://*.{SUBDOMAIN_BASE}",
                              cast=lambda value: value.split(","))
OVERRIDE_SCHEME = config("OVERRIDE_SCHEME",
                         default=None)
HOT_POSTS_SLICE = config("HOT_POSTS_SLICE",
                         default=12,
                         cast=int)
OAUTH2_PROVIDER = {
    "OIDC_ENABLED": True,
    "OIDC_RSA_PRIVATE_KEY": config("OIDC_RSA_PRIVATE_KEY",
                                   default=None,
                                   cast=oidc_rsa_private_key_cast),
    "SCOPES": {
        "openid": "OpenID Connect",
    },
    "OAUTH2_VALIDATOR_CLASS": "rollsocialnetwork.oauth2_validators.RollOAuth2Validator",
    "OIDC_ISS_ENDPOINT": config("OIDC_ISS_ENDPOINT",
                                default=None)
}
GEOIP_PATH = config("GEOIP_PATH",
                    default="./.geoip")
OIDC_ENDPOINT = config("OIDC_ENDPOINT",
                       default=f"https://{SUBDOMAIN_BASE}/oauth2")
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_ROLL_KEY = config("SOCIAL_AUTH_ROLL_KEY",
                              default=None)
SOCIAL_AUTH_ROLL_SECRET = config("SOCIAL_AUTH_ROLL_SECRET",
                                 default=None)
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "rollsocialnetwork.oidc.pipeline.associate_roll_user",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
]
SOCIAL_AUTH_URL_NAMESPACE = "socialauth"
ROLL_OAUTH2_APPLICATION_ID = config("ROLL_OAUTH2_APPLICATION_ID",
                                    cast=lambda x: x and int(x),
                                    default=None)
ROLL_APPLICATION_REDIRECT_URI_TEMPLATE = config("ROLL_APPLICATION_REDIRECT_URI_TEMPLATE",
                                                default="https://{domain}/social/complete/roll/")
USE_X_FORWARDED_HOST = config("USE_X_FORWARDED_HOST",
                              default=True,
                              cast=bool)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ]
}
SSO_APP_URL = config("SSO_APP_URL",
                     default=None)
SSO_APP_AUTHORIZE_URL = config("SSO_APP_AUTHORIZE_URL",
                               default=(f"{SSO_APP_URL}/authorize" if SSO_APP_URL else None))
