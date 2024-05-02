from django.contrib.auth import get_user_model
from django.db.models import (CASCADE, CheckConstraint, F, ForeignKey, Model,
                              Q, UniqueConstraint)

User = get_user_model()


class Follow(Model):
    """Describes follow model."""

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='No duplicate subscription'
            ),
            CheckConstraint(
                check=~Q(author=F("user")),
                name='No self subscription'
            ),
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
