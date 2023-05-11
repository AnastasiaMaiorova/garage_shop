from django.db import models
from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE),
    is_active = models.BooleanField(default=True, verbose_name='Активность пользователя'),
    # customer_orders = models.ManyToManyField('Order', blank=True, verbose_name='Заказы покупателя', related_name='related_customer')
    # wishlist = models.ManyToManyField('Product', blank=True, verbose_name='Список ожидаемого')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        return "Пользователь {}".format(self.user.first_name)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'


