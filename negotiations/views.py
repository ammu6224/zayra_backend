from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PriceOffer
from .serializers import PriceOfferSerializer
from orders.models import Order


class PriceOfferViewSet(viewsets.ModelViewSet):

    serializer_class = PriceOfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_vendor:
            return PriceOffer.objects.filter(
                product__vendor=user
            ).select_related("product", "customer")

        return PriceOffer.objects.filter(
            customer=user
        ).select_related("product", "product__vendor")

    def perform_create(self, serializer):
        serializer.save(
            customer=self.request.user,
            status="pending"
        )

    # 🔥 VENDOR ACCEPT OFFER
    @action(detail=True, methods=["post"])
    def accept(self, request, pk=None):

        offer = self.get_object()

        # only vendor can accept
        if offer.product.vendor != request.user:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        offer.status = "accepted"
        offer.save()

        # 🔥 CREATE ORDER AUTOMATICALLY
        order = Order.objects.create(
            customer=offer.customer,
            product=offer.product,
            quantity=1,
            total_price=offer.offered_price,
            status="pending"
        )

        return Response({
            "message": "Offer accepted",
            "order_id": order.id
        })

    # ❌ REJECT OFFER
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):

        offer = self.get_object()

        if offer.product.vendor != request.user:
            return Response(
                {"error": "Not allowed"},
                status=status.HTTP_403_FORBIDDEN
            )

        offer.status = "rejected"
        offer.save()

        return Response({
            "message": "Offer rejected"
        })