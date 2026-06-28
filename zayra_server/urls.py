from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # AUTH
    path("api/auth/", include("accounts.urls")),

    # PRODUCTS
    path("api/products/", include("products.urls")),

    # CART
    path("api/cart/", include("cart.urls")),

    # ORDERS
    path("api/orders/", include("orders.urls")),

    # CHAT
    path("api/chat/", include("chat.urls")),

    # NEGOTIATION
    path("api/negotiation/", include("negotiations.urls")),

    # REVIEWS
    path("api/reviews/", include("reviews.urls")),

    # RETURNS
    path("api/returns/", include("returns.urls")),

    # PAYMENTS
    path("api/payments/", include("payments.urls")),

    # CORE
    path("api/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )