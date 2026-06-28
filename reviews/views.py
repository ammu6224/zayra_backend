from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly
)

from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):

        product_id = self.request.query_params.get(
            "product"
        )

        if product_id:
            return Review.objects.filter(
                product_id=product_id
            ).order_by("-created_at")

        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(
            customer=self.request.user
        )