import re

from django.db import models
from django.urls import reverse


class BlackListType(models.Model):
    """ Класс модели типа ЧС """
    id = models.AutoField('id', primary_key=True)
    name = models.CharField('Наименование типа ЧС', max_length=200, db_index=True)
    slug = models.SlugField('Slug', max_length=200, unique=True, db_index=True)

    class Meta:
        verbose_name = 'BlackListType'
        verbose_name_plural = 'BlackListTypes'
        # ordering = ['status_id', 'status_name']

    def __str__(self):
        # return f'status_id: {self.status_id}, status_name: {self.status_name}'
        return self.name

    def get_absolute_url(self):
        """ Процедура возвращает абсолюбный маршрут на конкрктную запись, котрый можно использовать в шаблоне """
        # return reverse('orders_by_status', kwargs={'status_id': self.status_id})
        # return reverse('orders_by_status', kwargs={'status_slug': self.slug})

        # return reverse('numbers_by_types', kwargs={'id': self.id})
        return reverse('numbers_by_types', kwargs={'type_slug': self.slug})


class BlackListNumber(models.Model):
    """ Класс модели черного списка номеров """
    id = models.AutoField('ID', primary_key=True)
    date_add = models.DateTimeField('Дата добавления', auto_now_add=True)
    type = models.ForeignKey('BlackListType', verbose_name='Тип ЧС', default=1, db_index=True,
                             on_delete=models.PROTECT)
    number = models.CharField('Номер телефона', max_length=20, unique=True, db_index=True)
    slug = models.SlugField('Slug', max_length=200, unique=True, db_index=True)
    comment = models.TextField('Комментарий', null=True, blank=True)
    user = models.CharField('Пользователь', max_length=36, db_index=True)

    class Meta:
        verbose_name = 'BlackListNumber'
        verbose_name_plural = 'BlackListNumbers'
        # ordering = ['status_id', 'status_name']

    def get_absolute_url(self):
        """ Процедура возвращает абсолюбный маршрут на конкрктную запись, котрый можно использовать в шаблоне """
        # return reverse('orders_by_status', kwargs={'status_id': self.status_id})
        return reverse('number', kwargs={'slug': self.slug})

    # Переопределяем метод save
    def save(self, *args, **kwargs):
        # Формируем слаг из номера
        self.slug = (''.join(re.findall('[0-9]+', self.number)))
        super(BlackListNumber, self).save(*args, **kwargs)
