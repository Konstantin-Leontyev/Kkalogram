from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey, Model

from recipes.models import Recipe

User = get_user_model()


class UserRecipeModel(Model):
    """Describes base model for user recipe relation."""

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
        """Describes cart model metaclass."""

        abstract = True
