from django.contrib import admin
from .models import Product, Order, Review, Item, ProductCollection

class ItemInline(admin.TabularInline):
    model = Item

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemInline,]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    pass