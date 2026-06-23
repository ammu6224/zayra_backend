from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentication
    path("api/auth/", include("accounts.urls")),

    # Products
    path("api/products/", include("products.urls")),

    # Cart
    path("api/cart/", include("cart.urls")),

    # Orders
    path("api/orders/", include("orders.urls")),

    # Chat
    path("api/chat/", include("chat.urls")),

    # Negotiation
    path("api/negotiation/", include("negotiation.urls")),

    # Core APIs (Admin + Vendor Dashboard)
    path("api/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )