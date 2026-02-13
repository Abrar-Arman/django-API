from django.contrib.auth import  get_user_model
from rest_framework import serializers

from ..models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["bio", "profile_picture", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["profile_picture"]