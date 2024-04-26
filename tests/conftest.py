import os
from pathlib import Path

import rest_framework
from django.utils.version import get_version
from dotenv.main import load_dotenv

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


assert get_version() < '4.0.0', 'Пожалуйста, используйте версию Django < 4.0.0'
assert rest_framework.VERSION == '3.12.4', 'Пожалуйста, используйте версию Django REST framework < 3.12.4'
# print(rest_framework.VERSION)
# print()

# pytest_plugins = [
#     'backend.users.tests.fixtures.fixture_user.py',
# ]