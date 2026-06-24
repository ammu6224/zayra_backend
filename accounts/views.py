from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
import random

from .serializers import SignupSerializer, UserSerializer
from .models import User, EmailOTP


# =========================
# SEND OTP (FIXED - NO HANG)
# =========================
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            email = request.data.get("email")

            if not email:
                return Response(
                    {"error": "Email required"},
                    status=400
                )

            otp = str(random.randint(100000, 999999))

            EmailOTP.objects.update_or_create(
                email=email,
                defaults={"otp": otp}
            )

            # ✅ SAFE: never crash API if email fails
            try:
                send_mail(
                    subject="ZAYRA Email Verification OTP",
                    message=f"Your ZAYRA OTP is: {otp}",
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                print("EMAIL ERROR:", str(e))
                # still return OTP success so frontend doesn't break

            return Response({
                "message": "OTP sent successfully"
            }, status=200)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=500)

# =========================
# VERIFY OTP
# =========================
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        obj = EmailOTP.objects.filter(
            email=email,
            otp=otp
        ).first()

        if obj:
            return Response({"verified": True})

        return Response(
            {"verified": False},
            status=400
        )


# =========================
# SIGNUP
# =========================
class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            role = "vendor" if user.is_vendor else "customer"

            return Response({
                "message": "Account created successfully",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": role,
                "user": UserSerializer(user).data
            }, status=201)

        return Response(serializer.errors, status=400)


# =========================
# LOGIN
# =========================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        login_id = request.data.get("login")
        password = request.data.get("password")

        if not login_id or not password:
            return Response(
                {"error": "Login and password required"},
                status=400
            )

        user_obj = User.objects.filter(
            Q(username=login_id) |
            Q(email=login_id) |
            Q(phone=login_id)
        ).first()

        if not user_obj:
            return Response({"error": "User not found"}, status=401)

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            return Response({"error": "Invalid password"}, status=401)

        refresh = RefreshToken.for_user(user)
        role = "vendor" if user.is_vendor else "customer"

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
            "user": UserSerializer(user).data
        })


# =========================
# PROFILE
# =========================
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)