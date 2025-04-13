from typing import Any, Dict, cast
from uuid import UUID

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from users.models import (Group, GroupMembership,  # or your actual import path
                          User)


class RegisterAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

    def validate_username(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value
    



class JoinGroupSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    device_id = serializers.CharField(required=True)

    def validate_device_id(self, value: UUID) -> UUID:
        # Add any device_id format validation here if needed
        if not str(value).strip():
            raise serializers.ValidationError("Device ID cannot be blank.")
        return value

class JoinGroupWithInviteSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate_token(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Token cannot be blank.")
        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super().get_token(user)

        # Tell the type checker this is our custom User
        actual_user = cast(User, user)

        try:
            membership = GroupMembership.objects.get(
                user=actual_user, role='admin')
            token['group_id'] = str(membership.group.id)
            token['role'] = 'admin'
        except GroupMembership.DoesNotExist:
            raise AuthenticationFailed("Only admins can log in.")

        return token

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        data = super().validate(attrs)

        try:
            membership = GroupMembership.objects.get(
                user=self.user, role='admin')
        except GroupMembership.DoesNotExist:
            raise AuthenticationFailed("Only admins can log in.")

        data['group_id'] = str(membership.group.id)
        data['group_name'] = membership.group.name
        data['role'] = 'admin'
        data['username'] = self.user.username  # type: ignore

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'created_at']
