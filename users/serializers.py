from uuid import UUID
from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Group name cannot be empty.")
        if Group.objects.filter(name=value).exists():
            raise serializers.ValidationError("Group already exists.")
        return value


class JoinGroupSerializer(serializers.Serializer):
    name = serializers.CharField(required=False, allow_blank=True)
    device_id = serializers.CharField(required=True)

    def validate_device_id(self, value: UUID) -> UUID:
        # Add any device_id format validation here if needed
        if not str(value).strip():
            raise serializers.ValidationError("Device ID cannot be blank.")
        return value
