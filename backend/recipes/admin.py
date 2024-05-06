from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe model admin site registration class."""

    list_display = ['name', 'author']
    list_filter = ['author', 'name', 'tags']