from django.urls import path

from .views import (
    SignupView,
    LoginView,
    ProfileView
)

from .views_vendor import VendorDashboardView

urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("profile/", ProfileView.as_view()),

    # Vendor Dashboard
    path(
        "vendor/dashboard/",
        VendorDashboardView.as_view(),
        name="vendor-dashboard"
    ),
]