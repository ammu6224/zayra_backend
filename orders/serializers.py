from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.name",
        read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"   # ⚠ FIXED (was _all_)
        read_only_fields = [
            "customer",
            "created_at"
        ]