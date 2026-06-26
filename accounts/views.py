from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from django.conf import settings
import random
import traceback

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from .serializers import SignupSerializer, UserSerializer
from .models import User, EmailOTP


# =========================
# SEND OTP
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

            print("===================================")
            print("SENDING OTP TO:", email)
            print("OTP:", otp)
            print("BREVO API FOUND:",
                  settings.BREVO_API_KEY is not None)
            print("===================================")

            # Configure Brevo API
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = settings.BREVO_API_KEY

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": email}],
                sender={
                    "email": "zayraofficial024@gmail.com",
                    "name": "Zayra"
                },
                subject="Zayra Email Verification OTP",
                html_content=f"""
                <html>
                    <body>
                        <h2>Zayra Email Verification</h2>

                        <p>Your OTP is:</p>

                        <h1 style="color:blue;">
                            {otp}
                        </h1>

                        <p>
                            This OTP is valid for
                            <b>10 minutes</b>.
                        </p>

                        <p>
                            Do not share this OTP
                            with anyone.
                        </p>

                        <br>

                        <p>
                            Thanks,<br>
                            Team Zayra
                        </p>
                    </body>
                </html>
                """
            )

            api_instance.send_transac_email(send_smtp_email)

            print("EMAIL SENT SUCCESSFULLY")

            return Response(
                {"message": "OTP sent successfully"},
                status=200
            )

        except ApiException as e:
            print("BREVO API ERROR:", str(e))
            traceback.print_exc()

            return Response(
                {
                    "error": str(e),
                    "message": "Failed to send OTP"
                },
                status=500
            )

        except Exception as e:
            print("GENERAL ERROR:", str(e))
            traceback.print_exc()

            return Response(
                {
                    "error": str(e),
                    "message": "Failed to send OTP"
                },
                status=500
            )


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
        print("================================")
        print("LOGIN REQUEST")
        print("LOGIN ID:", login_id)
        print("PASSWORD:", password)
        print("================================")

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
            return Response(
                {"error": "User not found"},
                status=401
            )
        print("================================")
        print("USER FOUND:", user_obj.username)
        print("EMAIL:", user_obj.email)
        print("IS VENDOR:", user_obj.is_vendor)
        print(
            "CHECK PASSWORD:",
            user_obj.check_password(password)
        )
        print("================================")
        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if not user:
            return Response(
                {"error": "Invalid password"},
                status=401
            )

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