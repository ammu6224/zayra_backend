from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from orders.models import Order
from products.models import Product


User = get_user_model()


# -----------------------------
# 📊 ADMIN DASHBOARD STATS
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_dashboard(request):

    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Product.objects.count()

    delivered_orders = Order.objects.filter(status="delivered")

    total_revenue = sum(o.total_price for o in delivered_orders)

    vendors = User.objects.filter(role="vendor").count()
    customers = User.objects.filter(role="customer").count()

    return Response({
        "total_users": total_users,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_revenue": float(total_revenue),
        "vendors": vendors,
        "customers": customers,
    })


# -----------------------------
# 📦 ALL ORDERS (ADMIN VIEW)
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_orders(request):

    orders = Order.objects.all().order_by("-created_at")

    data = []

    for o in orders:
        data.append({
            "order_id": o.id,
            "customer": o.customer.username,
            "product": o.product.name,
            "vendor": o.product.vendor_id,
            "quantity": o.quantity,
            "price": o.total_price,
            "status": o.status,
            "date": o.created_at,
        })

    return Response(data)


# -----------------------------
# 🛍️ ALL PRODUCTS (ADMIN VIEW)
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_products(request):

    products = Product.objects.all()

    data = []

    for p in products:
        data.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "vendor": p.vendor_id,
        })

    return Response(data)


# -----------------------------
# 👤 ALL USERS (ADMIN VIEW)
# -----------------------------
@api_view(["GET"])
@permission_classes([IsAdminUser])
def admin_users(request):

    users = User.objects.all()

    data = []

    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "role": getattr(u, "role", "unknown"),
            "email": u.email,
        })

    return Response(data)