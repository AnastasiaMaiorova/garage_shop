from django.db import models
from django.conf import settings

# Пользователь
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


# Категория
class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name="Категория")
    slug = models.SlugField(unique=True)  # ссылка категории

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


# Продукт
class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)# on_delete=models.CASCADE - для удаления объекта
    name_product = models.CharField(max_length=255, verbose_name="Наименование")
    artikul = models.CharField(max_length=255, verbose_name="Артикул")
    slug = models.SlugField(unique=True)  # ссылка на продукт
    image = models.ImageField(upload_to='media', verbose_name="Фотография")
    description = models.TextField(null=True, verbose_name="Описание товара")# null=True описание может и не быть
    manufacturer = models.CharField(max_length=255, verbose_name="Производитель")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")# max_digits=10 - максимальная длина числа до запятой, decimal_places=2 - количесво чисел после запятой

    def __str__(self):
        return self.name_product

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


# Продукт -> Масло
class Oil(Product):

    valume = models.CharField(max_length=255, verbose_name='Объем')

    def __str__(self):
        return "{} {}".format(self.category.name, self.name_product)

    class Meta:
        verbose_name = 'Масло'
        verbose_name_plural = 'Масла'


# Продукт -> Фильтр
class Filter(Product):
    size = models.CharField(max_length=255, verbose_name='Размер')

    def __str__(self):
        return "{} {}".format(self.category.name, self.name_product)

    class Meta:
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтра'


