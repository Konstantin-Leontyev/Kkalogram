from django.contrib import admin

from .models import Recipe, RecipeIngredient


class IngredientInline(admin.TabularInline):
    """Describes recipe ingredients inline class ."""
    model = RecipeIngredient
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Recipe model admin site registration class."""
    list_display = ('name', 'author', 'is_favorited')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    inlines = [IngredientInline]

    @admin.display(description='Добавлен в избранное')
    def is_favorited(self, obj):
        """Returns in favorite count."""
        return obj.favorites.count()
