from rest_framework import serializers
from .models import ReturnRequest


class ReturnRequestSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.username",
        read_only=True
    )

    product_name = serializers.CharField(
        source="order.product.name",
        read_only=True
    )

    class Meta:
        model = ReturnRequest

        fields = [
            "id",
            "customer",
            "customer_name",
            "order",
            "product_name",
            "reason",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "customer",
            "customer_name",
            "product_name",
            "created_at",
        ]