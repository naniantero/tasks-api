# users/tests/test_register_admin.py
# pyright: reportAttributeAccessIssue=false

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Group, GroupMembership
from typing import Dict, Any, cast


class RegisterAdminTests(APITestCase):
    def test_register_admin_creates_user_group_and_membership(self) -> None:
        url = reverse("users:register_admin")

        response = self.client.post(
            url, data={"username": "parent1"}, format="json")

        # Status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data: Dict[str, Any] = cast(Dict[str, Any], response.data)

        # Response keys
        self.assertIn("access", data)
        self.assertIn("refresh", data)
        self.assertIn("group_id", data)
        self.assertIn("password", data)

        # Validate user
        user = User.objects.get(username="parent1")
        self.assertTrue(user)

        # Validate group
        group = Group.objects.get(id=data["group_id"])
        self.assertTrue(group)

        # Validate group membership
        membership = GroupMembership.objects.get(user=user, group=group)
        self.assertEqual(membership.role, "admin")
