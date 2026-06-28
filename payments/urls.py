from django.urls import path
from .views import create_payment_order, verify_payment

urlpatterns = [
    path(
        "create-order/",
        create_payment_order,
        name="create-order"
    ),

    path(
        "verify/",
        verify_payment,
        name="verify-payment"
    ),
]