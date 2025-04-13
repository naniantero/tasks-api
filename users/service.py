# pyright: reportAttributeAccessIssue=false
import uuid
from datetime import timedelta
from typing import Any, Dict

from django.utils.crypto import get_random_string
from django.utils.timezone import now
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken, Token

from users.models import Group, GroupMembership, User

JOIN_TOKEN_EXPIRY = timedelta(days=3)


def register_admin_and_create_group(username: str) -> Dict[str, Any]:
    group_name = "My family"
    group = Group.objects.create(name=group_name)
    password = get_random_string(12)

    # Create user and assign to group
    user = User.objects.create_user(
        username=username,
        password=password,
    )
    GroupMembership.objects.create(
        user=user,
        group=group,
        role='admin',
    )

    # Generate token with group_id and role baked in
    refresh = RefreshToken.for_user(user)
    refresh["group_id"] = str(group.id)
    refresh["role"] = "admin"

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "group_id": str(group.id),
        "password": password,
        "username": username,
    }


def admin_join_group(group_id: uuid.UUID, device_id: str, name: str) -> User | None:
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


def join_group_with_invite(token: Token) -> User | None:
    try:
        access_token = AccessToken(token)
        group_id = access_token['group_id']
        name = access_token['name']
    except Exception:
        return None

    group = Group.objects.get(id=group_id)
    user = User.objects.create(
        username=name
    )
    GroupMembership.objects.get_or_create(
        user=user, group=group, role='member')

    return User.objects.get(id=user.id)


def generate_invite_link(group_id: str, name: str) -> str:
    """
    Generate an invite link for a group.
    """
    token = _generate_invite_token(group_id, name)
    return f"https://example.com/join/{group_id}/{token}/"


def _generate_invite_token(group_id: str, name: str) -> str:
    token = AccessToken()
    token['group_id'] = group_id
    token['name'] = name
    token.set_exp(from_time=now(), lifetime=JOIN_TOKEN_EXPIRY)
    return str(token)
