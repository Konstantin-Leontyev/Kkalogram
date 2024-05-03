from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag model admin site registration class."""

    list_display = ['name', 'slug', 'color']
