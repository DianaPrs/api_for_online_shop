from django.conf import settings
from django.db import models


class Product(models.Model):
    """Товар."""
    name = models.CharField(verbose_name='Title', max_length=128)
    description = models.TextField(default='')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

class OrderStatusChoices(models.TextChoices):
    """Статусы заказа."""

    NEW = "NEW ", "Новый"
    IN_PROGRESS = "IN_PROGRESS ", "В процессе"
    DONE = "DONE", "Закрыт"

class Order(models.Model):
    """Заказ."""
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    products = models.ManyToManyField(Product, through='Item')
    status = models.TextField(
        choices=OrderStatusChoices.choices,
        default=OrderStatusChoices.NEW 
    )
    total_price = models.PositiveIntegerField(default=0)   
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE) #related_name='section_is_main')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)   


class Review(models.Model):
    """Отзыв."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    RATING = [(ONE, 1), (TWO, 2), (THREE, 3), (FOUR, 4), (FIVE, 5),]
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    text = models.TextField(default='')
    rating = models.IntegerField(
        choices=RATING,
        default=FIVE
    )    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    

class ProductCollection(models.Model):
    """Подборки."""
    headline = models.CharField(max_length=200) 
    text = models.TextField(default='')
    items = models.ManyToManyField(Product)
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    