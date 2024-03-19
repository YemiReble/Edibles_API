from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from .models import OneTimePassword, Account as User
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework import status
from datetime import datetime


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            **validated_data
        )
        return user

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        request = self.context.get("request")
        user = User.objects.get(email=email)
        token = user.tokens()

        return {
            "email": user.email,
            "access_token": token.get("access"),
            "refresh_token": token.get("refresh"),
        }
