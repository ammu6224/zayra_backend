from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q

from .serializers import SignupSerializer, UserSerializer
from .models import User


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
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# LOGIN (EMAIL / PHONE / USERNAME)
# =========================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        login_id = request.data.get("login")
        password = request.data.get("password")

        if not login_id or not password:
            return Response(
                {"error": "Login and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Find user using username OR email OR phone
        user_obj = User.objects.filter(
            Q(username=login_id) |
            Q(email=login_id) |
            Q(phone=login_id)
        ).first()

        if not user_obj:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # authenticate using username internally
        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        role = "vendor" if user.is_vendor else "customer"

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": role,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


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

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )