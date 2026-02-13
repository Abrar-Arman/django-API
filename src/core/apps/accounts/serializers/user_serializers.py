from django.contrib.auth import  get_user_model,password_validation
from rest_framework import serializers
from django.contrib.auth.hashers import check_password


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username','role', 'password', 'old_password']
        read_only_fields = ['role','id']  

    def create(self, validated_data):
        validated_data['role'] = 'instructor'
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password('MyDefault123!')
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        old_password = validated_data.pop('old_password', None)

        if password:
            if not old_password:
                raise serializers.ValidationError({"old_password": "This field is required to change password."})
            if not check_password(old_password, instance.password):
                raise serializers.ValidationError({"old_password": "Old password is incorrect."})
            password_validation.validate_password(password, instance)
            instance.set_password(password)

        email = validated_data.get('email', None)
        if email:
            instance.email = email

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
