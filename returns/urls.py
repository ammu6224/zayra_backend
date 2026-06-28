from django.urls import path
from .views import ReturnRequestListCreateView

urlpatterns = [
    path("", ReturnRequestListCreateView.as_view()),
]