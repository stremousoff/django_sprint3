from django.db import models


class PublishedCreated(models.Model):
    """Абстрактная модель для модели публикации.

    Содержит в себе поля разрешения на публикацию и дату создания.
    """

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True
