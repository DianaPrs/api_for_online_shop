from django.contrib.auth.models import User
from rest_framework import serializers

from online_shop.models import Product, Order, Review, ProductCollection


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для товара."""

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'created_at', 'updated_at',)

    
    def create(self, validated_data):
        """Метод для создания"""
        pass
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Метод для обновления"""
        pass
        return super().update(instance, validated_data)

class OrderSerializer(serializers.ModelSerializer):
    """Serializer для заказа."""
    creator = UserSerializer(
    read_only=True,
    )

    class Meta:
        model = Order
        fields = ('creator', 'products', 'status', 'total_price', 'created_at', 'updated_at',) 

    def create(self, validated_data):
        """Метод для создания"""
        pass
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Метод для обновления"""
        pass
        return super().update(instance, validated_data)

class ReviewSerializer(serializers.ModelSerializer):

    creator = UserSerializer(
    read_only=True,
    )

    class Meta:
        model = Review
        fields = ('creator', 'product_id', 'text', 'rating', 'created_at', 'updated_at',)
    
    def create(self, validated_data):
        """Метод для создания"""
        pass
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Метод для обновления"""
        pass
        return super().update(instance, validated_data)


class ProductCollectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductCollection
        fields = ('headline', 'text', 'items', 'created_at', 'updated_at',)