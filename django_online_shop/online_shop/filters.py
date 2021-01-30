from django_filters import rest_framework as filters
from online_shop.models import Product, Order, Review, ProductCollection

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
    """Фильтры для заказов.Заказы можно фильтровать по статусу / общей сумме / дате создания / дате обновления и продуктам из позиций."""
    pass

class ReviewFilter(filters.FilterSet):
    """Фильтры для отзывов. Отзыв можно фильтровать по ID пользователя, дате создания и ID товара."""
    pass

    creator = filters.NumberFilter() 
    product = filters.NumberFilter() 
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Review
        fields = ('creator', 'product', 'created_at',)
        

