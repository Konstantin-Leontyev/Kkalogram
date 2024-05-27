import csv

# from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from foodgram.settings import BASE_DIR
from ingredients.models import Ingredient
# from recipes.models import Recipe
from tags.models import Tag

# User = get_user_model()
CSV_ROOT = BASE_DIR / 'data'


class Command(BaseCommand):
    """
    To add new csv data:
    1. Add csv into data folder. A csv file should be named as it's model.
    2. Import model;
    3. Add model into tables dict. Key should be named as model in lower case.
    """
    help = 'loading ingredients from data in json'

    tables = {
        'ingredients': Ingredient,
        # 'recipe': Recipe,
        'tags': Tag,
        # 'users': User,
    }

    def handle(self, *args, **options):
        """Loading ingredients from csv file.'"""

        for table in self.tables:

            file_path = f'{CSV_ROOT}/{table}.csv'

            try:
                with open(file_path, mode="r", encoding="utf-8") as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    csv_data = [row for row in csv_reader]
            except FileNotFoundError:
                raise FileExistsError(
                    f'Ошибка {file_path} не найден'
                )
            else:
                class_instance = self.tables[table]

                self.create_object(
                    cls=class_instance,
                    csv_data=csv_data,
                    table=table,
                )

    def create_object(self, cls, csv_data, table):
        """Create object in database using data from csv file. """
        message = f'importing {table}.csv please wait ...'
        self.print_info(message)

        for index, obj in enumerate(csv_data):
            cls.objects.create(**obj)
            if index == len(csv_data) - 1:
                message = f'{table}.cvs import successfully completed.'

        self.print_info(message)

    def print_info(self, message):
        """Print note if data has been successfully imported."""
        self.stdout.write(self.style.SUCCESS(message))
