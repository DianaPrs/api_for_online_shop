from django.shortcuts import render

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from online_shop.models import Product, Order, Review, ProductCollection
from .filters import  ProductFilter, ReviewFilter, OrderFilter
from .serializers import ProductSerializer, OrderSerializer, ReviewSerializer, ProductCollectionSerializer

class ProductViewSet(ModelViewSet):
    """ViewSet для товара."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    filterset_class = ProductFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]     
        return []

class OrderViewSet(ModelViewSet):
    """ViewSet для заказа"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()] 
        return []


class ReviweViewSet(ModelViewSet):
    """ViewSet для отзывов."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer 
    filterset_class = ReviewFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated()] 
        return []

class ProductCollectionViewSet(ModelViewSet):
    """ViewSet для подборок"""
    queryset = ProductCollection.objects.all()
    serializer_class = ProductCollectionSerializer

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]     
        return []