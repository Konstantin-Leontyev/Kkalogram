from core.models import UserRecipeModel


class Cart(UserRecipeModel):
    """Describes user cart relation tab."""

    class Meta:
        """Describes cart model metaclass."""

        default_related_name = 'cart'

        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
