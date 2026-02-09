from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import UserProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["email", "username", "password", "role"]

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class SetRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]

    def validate_role(self, value):
        allowed_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid role.")
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["role"] = self.user.role
        return data


# -------------------profile------------------


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_picture"]


# -------------------user------------------
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "role",
            "password",
            "old_password",
        ]
        read_only_fields = ["role", "id"]

    def create(self, validated_data):
        validated_data["role"] = "instructor"
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password("MyDefault123!")
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        old_password = validated_data.pop("old_password", None)

        if password:
            if not old_password:
                raise serializers.ValidationError(
                    {
                        "old_password": "This field is required to change password."
                    }
                )
            if not check_password(old_password, instance.password):
                raise serializers.ValidationError(
                    {"old_password": "Old password is incorrect."}
                )
            password_validation.validate_password(password, instance)
            instance.set_password(password)

        email = validated_data.get("email", None)
        if email:
            instance.email = email

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
