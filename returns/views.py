from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import ReturnRequest
from .serializers import ReturnRequestSerializer


class ReturnRequestListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = ReturnRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReturnRequest.objects.filter(
            customer=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)