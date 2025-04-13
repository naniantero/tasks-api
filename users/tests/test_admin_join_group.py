# pyright: reportAttributeAccessIssue=false

from typing import Any, Dict, cast

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Group, GroupMembership, User


class AdminJoinGroupTests(APITestCase):
    def setUp(self) -> None:
        self.group = Group.objects.create(name='Test Group')
        self.url = reverse('users:admin-join-group',
                           kwargs={'group_id': self.group.id})
        self.device_id = 'device_abc123'

    def test_join_group_with_existing_device_id_returns_same_user(self) -> None:
        # Create initial user for this device
        existing_user = User.objects.create(
            username='existing_user',
            device_id=self.device_id,
            first_name='Original'
        )

        # Join the group manually
        GroupMembership.objects.create(
            user=existing_user,
            group=self.group,
            role='member'
        )

        # Attempt to join the same group again using the same device_id
        data = {
            'device_id': self.device_id,
            'name': 'New Attempt Name'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(
            device_id=self.device_id).count(), 1)

        data = cast(Dict[str, Any], response.data)
        returned_user_id = data.get("user_id")
        self.assertEqual(returned_user_id, existing_user.id)
        self.assertEqual(returned_user_id, existing_user.id)

        # Check that membership still exists
        self.assertTrue(GroupMembership.objects.filter(
            user=existing_user,
            group=self.group,
            role='member'
        ).exists())
