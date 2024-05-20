from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (AllValuesMultipleFilter,
                                                   BooleanFilter)
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class AuthorFilter(SearchFilter):
    """Describes custom filter for recipe model author field."""

    search_param = 'author'


class IngredientFilter(SearchFilter):
    """
    Custom ingredient filter class.
    Overwrite default search_param from search to name.
    """

    search_param = 'name'


class RecipeFilter(FilterSet):
    """Describes custom filter for recipe model."""

    tags = AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        """Describes custom recipe model filter metaclass."""

        model = Recipe
        fields = ['tags']

    def filter_is_favorited(self, queryset, _, value):
        """Custom filter fo recipe is_favorite field."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, _, value):
        """Custom filter fo recipe is_in_shopping_cart field."""
        user = self.request.user
        if value and user.is_authenticated:
            return queryset.filter(cart__user=user)
        return queryset
