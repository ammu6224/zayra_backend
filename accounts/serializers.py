from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "is_vendor",
        )

        extra_kwargs = {
            "password": {
                "write_only": True
            }
        }

    def create(self, validated_data):
        is_vendor = validated_data.pop(
            "is_vendor",
            False
        )

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        if is_vendor:
            user.is_vendor = True
            user.is_customer = False
        else:
            user.is_vendor = False
            user.is_customer = True

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "is_vendor",
            "is_customer",
        )