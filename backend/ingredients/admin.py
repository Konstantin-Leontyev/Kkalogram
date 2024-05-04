from django.contrib.admin import ModelAdmin, register

from .models import Ingredient


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """Ingredient model admin site registration class."""

    list_display = ['name', 'measurement_unit']
    list_filter = ['name']
