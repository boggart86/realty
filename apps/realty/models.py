from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_photo_size(file):
    if file.size > settings.MAX_PHOTO_SIZE:
        raise ValidationError(f'Максимальный размер фото — {settings.MAX_PHOTO_SIZE} бит.')


class Realty(models.Model):
    TYPE_HOUSE = 'house'
    TYPE_CHOICES = [
        (TYPE_HOUSE, 'Дом/Коттедж'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='realty_objects',
        verbose_name='Владелец',
    )
    title = models.CharField(max_length=200, verbose_name='Название')
    realty_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default=TYPE_HOUSE, verbose_name='Тип',
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    address = models.CharField(max_length=300, verbose_name='Адрес')
    price = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Цена, ₽')
    area = models.DecimalField(max_digits=8, decimal_places=1, verbose_name='Площадь, м²')
    floors = models.PositiveSmallIntegerField(verbose_name='Этажей')
    rooms = models.PositiveSmallIntegerField(default=1, verbose_name='Комнат')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Объект недвижимости'
        verbose_name_plural = 'Объекты недвижимости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_cover_photo(self):
        return self.photos.order_by('order').first()

    def photos_count(self):
        return self.photos.count()


class RealtyPhoto(models.Model):
    realty = models.ForeignKey(
        Realty, on_delete=models.CASCADE, related_name='photos', verbose_name='Объект',
    )
    image = models.ImageField(
        upload_to='realty/%Y/%m/', validators=[validate_photo_size], verbose_name='Фото',
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фотографии'
        ordering = ['order']

    def __str__(self):
        return f'Фото {self.order} — {self.realty.title}'


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    realty = models.ForeignKey(
        Realty, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Объект',
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'realty')

    def __str__(self):
        return f'{self.user.email} → {self.realty.title}'
