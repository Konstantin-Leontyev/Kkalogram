from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Ingredient model admin site registration class."""

    list_display = ['name', 'measurement_unit']
    list_filter = ['name']
