from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import ModelMultipleChoiceFilter
from rest_framework.filters import SearchFilter
from tags.models import Tag

from .models import Recipe


class AuthorFilter(SearchFilter):
    search_param = 'author'


class RecipeFilter(FilterSet):
    """Describes custom filter for recipe model."""

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        """Describes custom recipe model filter metaclass."""

        model = Recipe
        fields = ['tags']
