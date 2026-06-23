from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(
        source="vendor.username",
        read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = [
            "vendor",
            "created_at",
            "updated_at"
        ]