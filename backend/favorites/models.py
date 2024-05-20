from core.models import UserRecipeModel


class Favorite(UserRecipeModel):
    """Describes favorite model class."""

    class Meta:
        """Describes favorite model metaclass."""

        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
