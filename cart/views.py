import uuid

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CartItem
from .serializers import CartItemSerializer
from orders.models import Order


class CartViewSet(viewsets.ModelViewSet):

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            customer=self.request.user
        ).select_related("product")

    def perform_create(self, serializer):
        serializer.save(
            customer=self.request.user
        )

    # 🔥 FIXED CHECKOUT LOGIC
    @action(detail=False, methods=["post"])
    def checkout(self, request):

        cart_items = CartItem.objects.filter(
            customer=request.user
        ).select_related("product")

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"},
                status=status.HTTP_400_BAD_REQUEST
            )

        group_id = str(uuid.uuid4())

        created_orders = []

        for item in cart_items:

            # ✅ USE PRODUCT PRICE (fallback system for now)
            final_price = item.product.price

            order = Order.objects.create(
                customer=request.user,
                product=item.product,
                quantity=item.quantity,
                total_price=final_price * item.quantity,
                status="pending",
                group_id=group_id
            )

            created_orders.append(order.id)

        # 🧹 CLEAR CART
        cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "group_id": group_id,
            "orders_created": created_orders
        })