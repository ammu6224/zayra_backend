from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Order
from products.models import Product


# -----------------------------
# 📊 VENDOR DASHBOARD SUMMARY
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_dashboard(request):

    vendor_id = request.user.id

    orders = Order.objects.filter(product__vendor_id=vendor_id)

    total_orders = orders.count()
    pending_orders = orders.filter(status="pending").count()
    shipped_orders = orders.filter(status="shipped").count()
    delivered_orders = orders.filter(status="delivered").count()

    earnings = sum(o.total_price for o in orders if o.status == "delivered")

    return Response({
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "earnings": float(earnings),
    })


# -----------------------------
# 📦 VENDOR ORDERS LIST
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_orders(request):

    vendor_id = request.user.id

    orders = Order.objects.filter(
        product__vendor_id=vendor_id
    ).order_by("-created_at")

    data = []

    for o in orders:
        data.append({
            "order_id": o.order_group_id,
            "product": o.product.name,
            "quantity": o.quantity,
            "price": o.total_price,
            "status": o.status,
            "customer": o.customer.username,
            "date": o.created_at,
        })

    return Response(data)


# -----------------------------
# 📦 VENDOR PRODUCTS LIST
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def vendor_products(request):

    vendor_id = request.user.id

    products = Product.objects.filter(vendor_id=vendor_id)

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "image": p.image.url if p.image else None,
        })

    return Response(data)