from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey, Model
from recipes.models import Recipe

User = get_user_model()


class Favorite(Model):
    """Describes favorite model class."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='Пользователь',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        """Describes favorite model metaclass."""

        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
