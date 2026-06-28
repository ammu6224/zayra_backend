from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source='customer.username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = [
            'customer',
            'created_at'
        ]