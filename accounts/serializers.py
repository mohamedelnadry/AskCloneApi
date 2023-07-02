from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                        value):
            raise serializers.ValidationError("Enter a valid email address")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exists")

        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        if user:
            Profile.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["description", "facebook", "twitter"]

    def update(self, validated_data):
        user = self.context["user"]
        profile = Profile.objects.filter(user=user.id).update(**validated_data)
        return profile
