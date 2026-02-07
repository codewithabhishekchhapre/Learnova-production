"""
User serializers for Learnova LMS
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from apps.core.serializers import BaseModelSerializer
from apps.core.validators import validate_email_format, validate_username_format
from .models import User, UserProfile


class UserProfileSerializer(BaseModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['organization', 'department', 'timezone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class UserSerializer(BaseModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'phone', 'avatar', 'bio', 'is_verified',
            'profile', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'role', 'is_verified', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'role', 'phone']

    def validate_email(self, value):
        validate_email_format(value)
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        validate_username_format(value)
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        attrs.pop('password_confirm')
        return attrs

    def create(self, validated_data):
        validated_data.setdefault('role', User.Role.STUDENT)
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
