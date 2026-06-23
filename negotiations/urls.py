from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriceOfferViewSet

router = DefaultRouter()
router.register(r"offers", PriceOfferViewSet, basename="offers")

urlpatterns = [
    path("", include(router.urls)),
]