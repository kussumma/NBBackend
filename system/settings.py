from pathlib import Path
import os
from datetime import timedelta

# use decouple
from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third party apps 
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'djoser',
    'rest_framework_simplejwt.token_blacklist',
    'social_django',
    'django_filters',

    # Local apps
    'apps.accounts',
    'apps.store',
    'apps.dashboard',
    'apps.cart',
    'apps.products',
    'apps.orders',
    'apps.shipping',
    'apps.coupons',
    'apps.payments',
    'apps.customers',
    'apps.blogs',
    'apps.search',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'system.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USERNAME'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOSTNAME'),
        'PORT': config('DB_PORT', cast=int),
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../', 'mediafiles')
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../', 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ORIGIN_ALLOW_ALL = True

# AUTHENTICATION
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
)

# DJOSER SETTINGS
DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SEND_ACTIVATION_EMAIL': True,
    'SET_PASSWORD_RETYPE': True,
    'SET_USERNAME_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SERIALIZERS': {},
    'SOCIAL_AUTH_TOKEN_STRATEGY': 'djoser.social.token.jwt.TokenStrategy',
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': ['http://localhost:3000/google'],
    'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY': config('GOOGLE_OAUTH2_KEY'),
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET': config('GOOGLE_OAUTH2_SECRET'),
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE': ['email', 'profile'],
    'SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA': ['first_name', 'last_name'],
}

# SIMPLE JWT
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'ecom-auth'
JWT_AUTH_REFRESH_COOKIE = 'ecom-refresh-auth'
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=3),
    'AUTH_HEADER_TYPES': ('Bearer','JWT'),
    'USER_ID_FIELD': 'email',
    'UPDATE_LAST_LOGIN': True,
}

# REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# CUSTOM USER MODEL
AUTH_USER_MODEL = 'accounts.User'

# EMAIL
SITE_ID = 1
SITE_NAME = '127.0.0.1:8000'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL')
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = config('TIME_ZONE')
USE_I18N = True
USE_TZ = True