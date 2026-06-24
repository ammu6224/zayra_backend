from django.urls import path

from .views import (
    SignupView,
    LoginView,
    ProfileView,
    SendOTPView,
    VerifyOTPView,
)

from .views_vendor import VendorDashboardView


urlpatterns = [

    # OTP APIs
    path(
        "send-otp/",
        SendOTPView.as_view(),
        name="send-otp"
    ),

    path(
        "verify-otp/",
        VerifyOTPView.as_view(),
        name="verify-otp"
    ),

    # Auth APIs
    path(
        "signup/",
        SignupView.as_view(),
        name="signup"
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "profile/",
        ProfileView.as_view(),
        name="profile"
    ),

    # Vendor Dashboard
    path(
        "vendor/dashboard/",
        VendorDashboardView.as_view(),
        name="vendor-dashboard"
    ),
]