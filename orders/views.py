import uuid
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # ✅ Vendor sees ONLY orders of their products
        if user.is_vendor:
            return Order.objects.filter(
                product__vendor=user
            ).select_related("product", "customer").order_by("-created_at")

        # ✅ Customer sees ONLY their own orders
        return Order.objects.filter(
            customer=user
        ).select_related("product", "product__vendor").order_by("-created_at")

    def perform_create(self, serializer):

        # 🔥 Group ID for tracking checkout session
        group_id = str(uuid.uuid4())

        serializer.save(
            customer=self.request.user,
            group_id=group_id
        )