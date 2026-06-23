from rest_framework.routers import DefaultRouter
from .views import PriceOfferViewSet

router = DefaultRouter()
router.register("offers", PriceOfferViewSet)

urlpatterns = router.urls