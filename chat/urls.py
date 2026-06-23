from rest_framework.routers import DefaultRouter
from .views import ChatViewSet

router = DefaultRouter()
router.register("messages", ChatViewSet)

urlpatterns = router.urls