from django.db import models

from config import settings
from users.models import NULLABLE


class Ad(models.Model):
    """Модель объявления."""

    title = models.CharField(
        max_length=255, verbose_name='Название товара',
        help_text='Введите название товара')
    price = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name='Цена товара',
        help_text='Укажите цену товара')
    description = models.TextField(
        verbose_name='Описание товара',
        **NULLABLE,
        help_text='Введите описание товара')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор объявления',
        on_delete=models.CASCADE,
        related_name='announcement')
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания объявления',
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время обновления объявления',
        **NULLABLE,
        editable=False
    )
    image = models.ImageField(
        upload_to='ads/images/',
        verbose_name='Изображение',
        **NULLABLE,
        help_text='Загрузите изображение'
    )

    def __str__(self):
        return f'{self.title} - {self.price}'

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Review(models.Model):
    """Модель отзыва о товаре"""

    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Введите отзыв')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор отзыва',
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews_written'
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        verbose_name='Объявление',
        related_name='reviews'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата и время создания отзыва',
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата и время обновления отзыва',
        **NULLABLE,
        editable=False
    )

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
