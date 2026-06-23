from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import Order
from products.models import Product

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_dashboard(request):

vendor = request.user

orders = Order.objects.filter(
    product__vendor=vendor
)

total_orders = orders.count()

pending_orders = orders.filter(
    status="pending"
).count()

accepted_orders = orders.filter(
    status="accepted"
).count()

shipped_orders = orders.filter(
    status="shipped"
).count()

delivered_orders = orders.filter(
    status="delivered"
).count()

total_products = Product.objects.filter(
    vendor=vendor
).count()

earnings = sum(
    float(order.total_price)
    for order in orders
    if order.status == "delivered"
)

return Response({
    "vendor": vendor.username,
    "total_products": total_products,
    "total_orders": total_orders,
    "pending_orders": pending_orders,
    "accepted_orders": accepted_orders,
    "shipped_orders": shipped_orders,
    "delivered_orders": delivered_orders,
    "earnings": earnings
})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_orders(request):

vendor = request.user

orders = Order.objects.filter(
    product__vendor=vendor
).order_by("-created_at")

data = []

for order in orders:

    data.append({
        "id": order.id,
        "group_id": order.group_id,
        "customer": order.customer.username,
        "product": order.product.name,
        "quantity": order.quantity,
        "price": str(order.total_price),
        "status": order.status,
        "created_at": order.created_at,
    })

return Response(data)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):

vendor = request.user

order = get_object_or_404(
    Order,
    id=order_id,
    product__vendor=vendor
)

new_status = request.data.get("status")

allowed_status = [
    "pending",
    "accepted",
    "shipped",
    "delivered",
    "cancelled"
]

if new_status not in allowed_status:
    return Response(
        {"error": "Invalid status"},
        status=400
    )

order.status = new_status
order.save()

return Response({
    "message": "Order status updated successfully",
    "order_id": order.id,
    "new_status": order.status
})