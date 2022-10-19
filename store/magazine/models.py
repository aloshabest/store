from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model


User = get_user_model()

class Category(MPTTModel):
    title = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children', db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    type = models.TextField(blank=True)

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('magazine:category', kwargs={'cat_slug': self.slug})


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = TreeForeignKey(Category, on_delete=models.PROTECT,  blank=True, null=True, related_name='products')
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image_first = models.ImageField(upload_to='photo/%Y/%m/%d', default=None, blank=True, verbose_name='Фото')
    image_second = models.ImageField(upload_to='photo/%Y/%m/%d', default=None, blank=True, null=True, verbose_name='Фото')
    image_third = models.ImageField(upload_to='photo/%Y/%m/%d', default=None, blank=True, null=True, verbose_name='Фото')

    class Meta:
        ordering = ('title',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('magazine:single', kwargs={'prod_slug': self.slug})


class Sale(models.Model):
    prod = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Скидка')
    sale = models.IntegerField(default=0, verbose_name='Сумма скидки')
    last_price = models.FloatField(default=0, verbose_name='Старая цена')
    new_price = models.FloatField(default=0, verbose_name='Новая цена')

    class Meta:
        ordering = ('sale',)
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Cart(models.Model):
    customer = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар', related_name='count_in_order', )
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество товара в заказе')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.customer}'

