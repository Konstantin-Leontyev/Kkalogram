import os
from datetime import timedelta
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv.main import load_dotenv

load_dotenv()

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split()

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

AUTH_USER_MODEL = 'users.User'

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DEBUG = os.getenv('DEBUG') == 'True'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJOSER = {
    'HIDE_USERS': False,
    # 'LOGIN_FIELD': 'email',
    'PERMISSIONS': {
        'user_list': [
            'rest_framework.permissions.AllowAny'
        ],
    },
    "SERIALIZERS": {
            # "user": "api.serializers.UserSerializer",
            "user_list": "api.serializers.UserSerializer",
            # "current_user": "api.serializers.UserSerializer",
            "user_create": "users.serializers.CustomUserCreateSerializer",
        },
}
# DJOSER = {
#     "LOGIN_FIELD": "email",
#     "HIDE_USERS": False,
#     "PERMISSIONS": {
#         "resipe": ("api.permissions.AuthorStaffOrReadOnly,",),
#         "recipe_list": ("api.permissions.AuthorStaffOrReadOnly",),
#         "user": ("api.permissions.OwnerUserOrReadOnly",),
#         "user_list": ("api.permissions.OwnerUserOrReadOnly",),
#     },
#     "SERIALIZERS": {
#         "user": "api.serializers.UserSerializer",
#         "user_list": "api.serializers.UserSerializer",
#         "current_user": "api.serializers.UserSerializer",
#         "user_create": "api.serializers.UserSerializer",
#     },
# }

INSTALLED_APPS = [
    'django.contrib.admin',
    'users.apps.UsersAuthConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'users.apps.UsersConfig',
]

LANGUAGE_CODE = 'ru-RU'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

ROOT_URLCONF = 'foodgram.urls'

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

STATIC_URL = '/static/'

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

TIME_ZONE = 'UTC'

WSGI_APPLICATION = 'foodgram.wsgi.application'

USERNAME_MAX_LENGTH = 150

USE_I18N = True

USE_L10N = True

USE_TZ = True
