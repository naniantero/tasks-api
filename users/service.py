# pyright: reportAttributeAccessIssue=false
import uuid

from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Group, GroupMembership, User
from users.serializers import GroupSerializer, JoinGroupSerializer


def create_group(name: str) -> Group:
    """
    Create a new group in the database.
    """
    group = Group.objects.create(name=name)
    return group


def join_group(group_id: int, device_id: str, name: str) -> User | None:
    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return None

    existing_user = User.objects.filter(device_id=device_id).first()
    if existing_user:
        return existing_user
    
    # Create a lightweight user
    username = f"user_{uuid.uuid4().hex[:8]}"
    user = User.objects.create(
        username=username, first_name=name, device_id=device_id)

    # Add to group
    GroupMembership.objects.create(
        user=user,
        group=group,
        role='member'
    )

    return user
