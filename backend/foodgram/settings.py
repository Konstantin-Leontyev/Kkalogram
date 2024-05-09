import os
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
    # {
    #     'NAME': 'users.validators.NumberValidator',
    # },
    # {
    #     'NAME': 'users.validators.UppercaseValidator',
    # },
    # {
    #     'NAME': 'users.validators.LowercaseValidator',
    # },
    # {
    #     'NAME': 'users.validators.SymbolValidator',
    # },
]

AUTH_USERNAME_VALIDATORS = [
    {
        'NAME': 'users.validators.MeValidator',
    },
]

AUTH_USER_MODEL = 'users.User'

BASE_DIR = Path(__file__).resolve().parent.parent

CORS_ORIGIN_ALLOW_ALL = False
CORS_URLS_REGEX = r'^/api/.*$'

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
    'LOGIN_FIELD': 'email',
    'PERMISSIONS': {
        'user': ('rest_framework.permissions.AllowAny',),
        'user_list': ('rest_framework.permissions.AllowAny',),
    },
    "SERIALIZERS": {
        'current_user': 'users.serializers.CustomUserSerializer',
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'users.apps.UsersAuthConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'corsheaders',
    'djoser',
    'followers.apps.FollowersConfig',
    'recipes.apps.RecipesConfig',
    'ingredients.apps.IngredientsConfig',
    'tags.apps.TagsConfig',
    'users.apps.UsersConfig',

]

LANGUAGE_CODE = 'ru-RU'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

ROOT_URLCONF = 'foodgram.urls'

SECRET_KEY = os.getenv('SECRET_KEY', get_random_secret_key())

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

USE_I18N = True

USE_L10N = True

USE_TZ = True
