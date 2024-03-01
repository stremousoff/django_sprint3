from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import MAX_FILD_LENGTH, SLICE_NAME
from core.models import IsPublishedCreatedAt

User = get_user_model()  # получение модели пользователя


class Category(IsPublishedCreatedAt):
    """Модель категории."""

    title = models.CharField('Заголовок', max_length=MAX_FILD_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:SLICE_NAME]


class Location(IsPublishedCreatedAt):
    """Модель местоположения."""

    name = models.CharField('Название места', max_length=MAX_FILD_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:SLICE_NAME]


class Post(IsPublishedCreatedAt):
    """Модель поста."""

    title = models.CharField('Заголовок', max_length=MAX_FILD_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:SLICE_NAME]
