from rest_framework.filters import SearchFilter


class IngredientFilter(SearchFilter):
    """
    Custom ingredient filter class.
    Overwrite default search_param from search to name.
    """

    search_param = 'name'
