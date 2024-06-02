import os
import sys
from datetime import timedelta
from pathlib import Path

from django.utils.translation import gettext_lazy as _
BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
SECRET_KEY = 'django-insecure-o9=$bv(+b=ng0&48zb6&4&ugmbh_(dt2$-t&#pnutdod&2cl25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # 'jazzmin',
    "admin_notification",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    # Third Party
    "ckeditor",
    "bootstrap4",
    # Custom Apps
    'import_export',
    "core",
    "api",
    "userauths",
    "modeltranslation",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
]

HOST = "luxeen.org"


NOTIFICATION_MODEL = 'userauths.Message'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = 'app.urls'


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "core.context_processor.default",
                "core.context_processor.banners",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pharmacy_db",
        "USER": "app",
        "PASSWORD": "@zarak@",
        "HOST": "db",
        "Port": "3306",
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGES = (("en", _("English")), ("ar", _("Arabic")), ("fr", _("French")))

LANGUAGE_CODE = "en"

TIME_ZONE = "Asia/Riyadh"

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOCALE_PATHS = (os.path.join(BASE_DIR, "locale/"),)


MODELTRANSLATION_DEFAULT_LANGUAGE = "en"
# Define the languages that your models will be translated into
MODELTRANSLATION_LANGUAGES = ("en", "ar", "fr")

# https://docs.djangoproject.com/en/3.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


JAZZMIN_SETTINGS = {
    'site_title': _("PharmacyOnline Care"),
    'site_header': _("PharmacyOnline Care Admin Dashboard"),
    'site_brand': _("PharmacyOnline Care"),
    "welcome_sign": "Welcome to the Admin Area of Pharmacy Online",
    'site_logo': "assets/imgs/theme/logo.png",
    'copyright': "pharmavcyonlinecare.com",
    "site_logo_classes": "img-circle",

    "show_ui_builder": False,
    "show_sidebar": False,
    "language_chooser": True,
    # - carousel
    "changeform_format": "carousel",
}
JAZZMIN_UI_TWEAKS = {
    "theme": "minty",
}


LOGIN_URL = "userauths:sign-in"
LOGIN_REDIRECT_URL = "core:index"
LOGOUT_REDIRECT_URL = "userauths:sign-in"
AUTH_USER_MODEL = "userauths.User"

CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {
        "skin": "moono",
        "codeSnippet_theme": "monokai",
        "toolbar": "all",
        "extraPlugins": ",".join(["codesnippet", "widget", "dialog"]),
    }
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=390),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
}


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'gswithmak@gmail.com'
EMAIL_HOST_PASSWORD = 'xdmp lgwz xzyb arbj'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000  # Adjust this number as needed


STATIC_URL = "/static/static/"
MEDIA_URL = "/static/media/"

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'
