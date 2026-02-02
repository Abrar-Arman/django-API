from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    class Meta:
        model = User
        fields = ['email', 'username', 'password','role']

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user
    

class SetRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']

    def validate_role(self, value):
        allowed_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in allowed_roles:
            raise serializers.ValidationError("Invalid role.")
        return value

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  
        data['role'] = self.user.role
        return data
    

#-------------------profile------------------


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


