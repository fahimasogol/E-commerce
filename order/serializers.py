from rest_framework import serializers
from .models import *


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    # This line defines a nested relationship within the Order serializer. Each Order can have multiple associated
    # OrderItem instances. The nested OrderItemSerializer allows the Order serializer to include a list of items
    # within each Order in the serialized output.
    class Meta:
        model = Order
        fields = '__all__'
