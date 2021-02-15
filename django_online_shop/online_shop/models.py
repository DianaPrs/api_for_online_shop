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

    NEW = "NEW", "Новый"
    IN_PROGRESS = "IN_PROGRESS", "В процессе"
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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True) 
    total_items = models.PositiveSmallIntegerField(default=0)     
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):
        self.total_price = sum(item.get_cost() for item in self.items.all())
        self.total_items = sum(item.quantity for item in self.items.all())
        super(Order, self).save(*args, **kwargs)


class Item(models.Model):
    """Позиция."""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveSmallIntegerField(default=0)   
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.product.name

    def get_cost(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.price
        super(Item, self).save(*args, **kwargs)
    


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
    