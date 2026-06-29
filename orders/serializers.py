from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    class Meta:
        model = Order

        fields = "__all__"

        read_only_fields = [
            "customer",
            "created_at",
            "group_id",
        ]