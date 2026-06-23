from django.urls import path

from .admin_api import (
admin_dashboard,
admin_orders,
admin_products,
admin_users
)

from .vendor_api import (
vendor_dashboard,
vendor_orders,
update_order_status
)

urlpatterns = [

# ADMIN APIs
path(
    "admin/dashboard/",
    admin_dashboard
),

path(
    "admin/orders/",
    admin_orders
),

path(
    "admin/products/",
    admin_products
),

path(
    "admin/users/",
    admin_users
),

# VENDOR APIs
path(
    "vendor/dashboard/",
    vendor_dashboard
),

path(
    "vendor/orders/",
    vendor_orders
),

path(
    "vendor/orders/<int:order_id>/status/",
    update_order_status
),

]