from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ReturnRequestViewSet,
    vendor_return_requests,
    update_return_status,
)

router = DefaultRouter()
router.register(
    "",
    ReturnRequestViewSet,
    basename="returns"
)

urlpatterns = [

    path(
        "",
        include(router.urls)
    ),

    path(
        "vendor/",
        vendor_return_requests
    ),

    path(
        "<int:pk>/status/",
        update_return_status
    ),
]