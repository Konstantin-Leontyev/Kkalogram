from core.models import UserRecipeModel


class Cart(UserRecipeModel):
    """Describes cart model class."""

    class Meta:
        """Describes cart model metaclass."""

        default_related_name = 'cart'

        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
