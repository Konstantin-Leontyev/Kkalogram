import os
from pathlib import Path

from dotenv.version import __version__ as dotenv_version
from dotenv.main import load_dotenv
from django import __version__ as django_version
from djoser import __version__ as djoser_version
from rest_framework import __version__ as rest_framework_version
from rest_framework_simplejwt import __version__ as rest_framework_simplejwt_version

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FILENAME = 'manage.py'
PROJECT_DIR_NAME = os.getenv('PROJECT_DIR_NAME')

for dir_name in (PROJECT_DIR_NAME,):
    path_to_dir = BASE_DIR / dir_name
    root_dir_content = os.listdir(BASE_DIR)
    if dir_name not in root_dir_content or not path_to_dir.is_dir():
        raise AssertionError(
            f'В директории `{BASE_DIR}` не найдена папка c проектом '
            f'`{dir_name}/`. Убедитесь, что у вас верная структура проекта.'
        )
    if dir_name == PROJECT_DIR_NAME:
        if FILENAME not in os.listdir(path_to_dir):
            assert False, (
                f'В директории `{path_to_dir}` не найден файл `{FILENAME}`. '
                f'Убедитесь, что у вас верная структура проекта.'
            )

required_django_version = '3.2.16'
required_rest_framework_version = '3.12.4'
required_framework_simplejwt_version = '4.7.2'
required_djoser_version = '2.1.0'
required_dotenv_version = '1.0.1'
required_django_cors_headers = '3.13.0'

assert django_version == required_django_version, (
    f'Пожалуйста, используйте версию Django {required_django_version}'
)
assert rest_framework_version == required_rest_framework_version, (
    f'Пожалуйста, используйте версию Django REST framework {required_rest_framework_version}'
)
assert rest_framework_simplejwt_version == required_framework_simplejwt_version,  (
    f'Пожалуйста, используйте версию simplejwt {required_framework_simplejwt_version}'
)
assert djoser_version == required_djoser_version, (
    f'Пожалуйста, используйте версию djoser {required_djoser_version}'
)
assert dotenv_version == required_dotenv_version, (
    f'Пожалуйста, используйте версию djoser {required_dotenv_version}'
)

# pytest_plugins = [
#     'fixtures.fixture_user.py',
# ]
