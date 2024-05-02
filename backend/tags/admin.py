from django.contrib import admin


class TagAdmin(admin.ModelAdmin):
    """Tag model admin site registration class."""

    list_display = ('name', 'slug', 'color')
