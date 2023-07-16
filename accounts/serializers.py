from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username Already Exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")
        return value

    def create(self, validated_data):
        """
        Create a new user with the validated data.
        """
        user = User.objects.create_user(**validated_data)
        if user:
            Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.Serializer):
    """
    Serializer for creating a user profile.
    """
    description = serializers.CharField()
    facebook = serializers.URLField(max_length=200)
    twitter = serializers.URLField(max_length=200)

    def create(self, validated_data):
        """
        Create a new profile with the validated data.
        """
        user = self.context["user"]
        profile, created = Profile.objects.get_or_create(user=user)
        for attr, value in validated_data.items():
            setattr(profile, attr, value)
        profile.save()

        return profile
