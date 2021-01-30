from django.contrib import admin
from .models import Product, Order, Review, Item, ProductCollection


class ItemInline(admin.TabularInline):
    model = Item
    raw_id_fields = ['product']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'creator', 'total_items']
    list_filter = ['created_at']
    inlines = [ItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(ProductCollection)
class ProductCollectionAdmin(admin.ModelAdmin):
    pass