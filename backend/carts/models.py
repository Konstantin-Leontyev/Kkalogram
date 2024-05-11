from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey, Model
from recipes.models import Recipe

User = get_user_model()


class Cart(Model):
    """Describes shopping cart model class."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        """Describes shopping cart model metaclass."""

        default_related_name = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'В корзине'
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'recipe'],
        #                             name='unique cart user')
        # ]
