from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework.filters import ModelMultipleChoiceFilter
from rest_framework.filters import SearchFilter

from tags.constants import SLUG_CHOICES
from .models import Recipe
from tags.models import Tag


class AuthorFilter(SearchFilter):
    search_param = 'author'


class RecipeFilter(FilterSet):
    """Describes custom filter for recipe model."""

    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        # to_field_name='tags',
        # conjoined=True,
        queryset=Tag.objects.all(),
    )

    # tags = MultipleChoiceFilter(
    #     choices=SLUG_CHOICES,
    #     action=lambda queryset, value:
    #     queryset.filter(recipe__tags__in=value)
    # )

    class Meta:
        """Describes custom recipe model filter metaclass."""

        model = Recipe
        fields = ['tags']
