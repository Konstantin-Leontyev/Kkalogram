from django.contrib.admin import ModelAdmin, register

from .models import Tag


@register(Tag)
class TagAdmin(ModelAdmin):
    """Tag model admin site registration class."""

    list_display = ['name', 'slug', 'color']
