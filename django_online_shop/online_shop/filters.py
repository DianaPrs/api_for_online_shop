from django_filters import rest_framework as filters
from online_shop.models import Product, Order, Item, Review, ProductCollection, OrderStatusChoices

class ProductFilter(filters.FilterSet):
    """Фильтры для товаров."""

    price_from= filters.NumberFilter(field_name='price', lookup_expr="gte")
    price_to= filters.NumberFilter(field_name='price', lookup_expr="lte")
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('name', 'description', 'price_from', 'price_to',)


class OrderFilter(filters.FilterSet):
    """Фильтры для заказов."""

    status = filters.ChoiceFilter(choices=OrderStatusChoices.choices) 
    price_from= filters.NumberFilter(field_name='total_price', lookup_expr="gte")
    price_to= filters.NumberFilter(field_name='total_price', lookup_expr="lte")
    products =  filters.CharFilter()
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ('status', 'price_from', 'price_to', 'products', 'created_at', 'updated_at',)

class ReviewFilter(filters.FilterSet):
    """Фильтры для отзывов. Отзыв можно фильтровать по ID пользователя, дате создания и ID товара."""

    creator = filters.NumberFilter() 
    product = filters.NumberFilter() 
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ('creator', 'product', 'created_at',)