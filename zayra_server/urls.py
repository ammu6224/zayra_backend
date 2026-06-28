from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ==========================
    # ADMIN
    # ==========================
    path("admin/", admin.site.urls),

    # ==========================
    # AUTHENTICATION
    # ==========================
    path("api/auth/", include("accounts.urls")),

    # ==========================
    # PRODUCTS
    # ==========================
    path("api/products/", include("products.urls")),

    # ==========================
    # CART
    # ==========================
    path("api/cart/", include("cart.urls")),

    # ==========================
    # ORDERS
    # ==========================
    path("api/orders/", include("orders.urls")),

    # ==========================
    # CHAT
    # ==========================
    path("api/chat/", include("chat.urls")),

    # ==========================
    # NEGOTIATIONS
    # ==========================
    path("api/negotiation/", include("negotiations.urls")),

    # ==========================
    # REVIEWS & RATINGS
    # ==========================
    path("api/reviews/", include("reviews.urls")),

    # ==========================
    # CORE APIs
    # ==========================
    path("api/", include("core.urls")),
]

# ==========================
# MEDIA FILES
# ==========================
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )