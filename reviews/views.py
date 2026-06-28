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

    queryset = Review.objects.all().order_by(
        "-created_at"
    )

    def get_queryset(self):

        product_id = self.request.query_params.get(
            "product"
        )

        queryset = Review.objects.all().order_by(
            "-created_at"
        )

        if product_id:
            queryset = queryset.filter(
                product_id=product_id
            )

        return queryset

    def perform_create(self, serializer):

        serializer.save(
            customer=self.request.user
        )