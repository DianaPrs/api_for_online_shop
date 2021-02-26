from django.contrib.auth.models import User
from rest_framework import serializers

from online_shop.models import Product, Order, Item, Review, ProductCollection


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username',)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer для товара."""

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'created_at', 'updated_at',)


class ItemSerializer(serializers.ModelSerializer):
    """Serializer для позиции."""

    product = serializers.PrimaryKeyRelatedField(
        queryset = Product.objects.all(),
        required=True) 
    
    class Meta:
        model = Item
        fields = ('product', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer для заказа."""

    creator = UserSerializer(read_only=True)
    positions = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'creator', 'positions', 'status', 'total_price', 'created_at', 'updated_at',) 
    
    def create(self, validated_data):
        """Метод создания заказа"""
        validated_data["creator"] = self.context["request"].user
        positions_data = validated_data.pop('positions')
        order = super().create(validated_data)

        raw_positions = []
        for position in positions_data:
            position = Item(order=order, 
            product=position["product"],
            quantity=position["quantity"],
            price=position["product"].price)
            raw_positions.append(position)
        Item.objects.bulk_create(raw_positions)
        return order

    def update(self, instance, validated_data):
        """Метод для обновления"""
        order = Order.objects.get(pk=instance.id)
        if order.status != validated_data['status'] and not self.context["request"].user.is_staff:
            raise serializers.ValidationError("Only admin can update status")
        return super().update(instance, validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer для отзыва."""
    creator = UserSerializer(read_only=True)
    product_id = serializers.CharField(read_only=False)

    class Meta:
        model = Review
        fields = ('id', 'creator', 'product_id', 'text', 'rating', 'created_at', 'updated_at',)
    
    def create(self, validated_data):
        """Метод для создания отзыва"""
        user = self.context["request"].user
        validated_data["creator"] = user
        review = Review.objects.filter(creator=user)
        if len(review) >= 1:
            raise serializers.ValidationError("User alredy left review")
        return super().create(validated_data)


class ProductCollectionSerializer(serializers.ModelSerializer):
    """Serializer для подборки."""
    class Meta:
        model = ProductCollection
        fields = ('id', 'headline', 'text', 'items', 'created_at', 'updated_at',)