from typing import Any

from django.contrib.auth import get_user_model
from rest_framework import serializers

from library_test_project.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class RegisterSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def create(self, validated_data: Any) -> User:
        instance = User.objects.create_user(**validated_data)
        return instance
