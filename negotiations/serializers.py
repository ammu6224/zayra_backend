from rest_framework import serializers
from .models import PriceOffer


class PriceOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceOffer
        fields = "__all__"