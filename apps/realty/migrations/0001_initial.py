from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import apps.realty.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Realty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('realty_type', models.CharField(
                    choices=[('house', 'Дом/Коттедж')],
                    default='house', max_length=20, verbose_name='Тип',
                )),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('address', models.CharField(max_length=300, verbose_name='Адрес')),
                ('price', models.DecimalField(decimal_places=2, max_digits=14, verbose_name='Цена, ₽')),
                ('area', models.DecimalField(decimal_places=1, max_digits=8, verbose_name='Площадь, м²')),
                ('floors', models.PositiveSmallIntegerField(verbose_name='Этажей')),
                ('rooms', models.PositiveSmallIntegerField(default=1, verbose_name='Комнат')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('owner', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='realty_objects',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Владелец',
                )),
            ],
            options={
                'verbose_name': 'Объект недвижимости',
                'verbose_name_plural': 'Объекты недвижимости',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RealtyPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(
                    upload_to='realty/%Y/%m/',
                    validators=[apps.realty.models.validate_photo_size],
                    verbose_name='Фото',
                )),
                ('order', models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')),
                ('realty', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='photos',
                    to='realty.realty',
                    verbose_name='Объект',
                )),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фотографии',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('realty', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorited_by',
                    to='realty.realty',
                    verbose_name='Объект',
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='favorites',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='Пользователь',
                )),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'unique_together': {('user', 'realty')},
            },
        ),
    ]
