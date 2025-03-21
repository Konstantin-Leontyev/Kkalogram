import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key
from dotenv.main import load_dotenv

load_dotenv()

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split()

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

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.getenv('DEBUG') == 'True'
PRODUCTION = os.getenv('PRODUCTION') == 'True'

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', 'django_db_name'),
            'USER': os.getenv('POSTGRES_USER', 'django_user'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'django_user_password'),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', 5432)
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJOSER = {
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.AllowAny',),
        'user_list': ('rest_framework.permissions.AllowAny',),

    },
    "SERIALIZERS": {
        'current_user': 'api.serializers.KkalogramUserSerializer',
        'user': 'api.serializers.KkalogramUserSerializer',
        'user_create': 'api.serializers.KkalogramUserCreateSerializer',
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'colorfield',
    'django_filters',
    'drf_yasg',
    'djoser',
    'rest_framework',
    'rest_framework.authtoken',

    'api.apps.ApiConfig',
    'carts.apps.CartsConfig',
    'core.apps.CoreConfig',
    'favorites.apps.FavoritesConfig',
    'followers.apps.FollowersConfig',
    'ingredients.apps.IngredientsConfig',
    'recipes.apps.RecipesConfig',
    'tags.apps.TagsConfig',
    'users.apps.UsersConfig',
]

LANGUAGE_CODE = 'ru-RU'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6,
}

ROOT_URLCONF = 'kkalogram.urls'

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

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

WSGI_APPLICATION = 'kkalogram.wsgi.application'

USE_I18N = True

USE_L10N = True

USE_TZ = True
