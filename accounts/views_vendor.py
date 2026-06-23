from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from orders.models import Order


class VendorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_vendor:
            return Response({"error": "Only vendors allowed"}, status=403)

        products = Product.objects.filter(vendor=request.user)

        orders = Order.objects.filter(
            product__vendor=request.user
        )

        total_earnings = sum(
            float(order.total_price)
            for order in orders
            if order.status == "delivered"
        )

        data = {
            "total_products": products.count(),
            "total_orders": orders.count(),
            "pending_orders": orders.filter(status="pending").count(),
            "delivered_orders": orders.filter(status="delivered").count(),
            "earnings": total_earnings,
        }

        return Response(data)