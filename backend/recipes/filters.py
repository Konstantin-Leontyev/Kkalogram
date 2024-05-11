from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import (BooleanFilter,
                                                   ModelMultipleChoiceFilter)
from rest_framework.filters import SearchFilter
from tags.models import Tag

from .models import Recipe


class AuthorFilter(SearchFilter):
    """Describes custom filter for recipe model author field."""

    search_param = 'author'


class RecipeFilter(FilterSet):
    """Describes custom filter for recipe model."""

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )
    is_favorited = BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')

    class Meta:
        """Describes custom recipe model filter metaclass."""

        model = Recipe
        fields = ['tags']

    def filter_is_favorited(self, queryset, _, value):
        """Custom filter fo recipe is_favorite field."""
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, _, value):
        """Custom filter fo recipe is_in_shopping_cart field."""
        if value and not self.request.user.is_anonymous:
            return queryset.filter(cart__user=self.request.user)
        return queryset
