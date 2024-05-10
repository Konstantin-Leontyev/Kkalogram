from django.contrib.auth import get_user_model
from django.db.models import CASCADE, ForeignKey, Model

User = get_user_model()


class Follow(Model):
    """Describes follow model class."""

    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Автор',
    )
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )

    class Meta:
        """Describes follow model metaclass."""

        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
