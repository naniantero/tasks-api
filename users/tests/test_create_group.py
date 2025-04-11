# pyright: reportAttributeAccessIssue=false

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import Group, User, GroupMembership


class CreateGroupWithAdminTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('users:group')

    def test_create_group_with_admin_success(self):
        data = {
            'group_name': 'Test Family',
            'admin_name': 'Test Parent'
        }
        response = self.client.post(self.url, data, format='json')

        # Check status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Extract response data
        group_id = response.data.get('group_id')
        admin_user_id = response.data.get('admin_user_id')

        # Check group was created
        self.assertTrue(Group.objects.filter(id=group_id).exists())

        # Check user was created
        user = User.objects.get(id=admin_user_id)
        self.assertEqual(user.first_name, 'Test Parent')
        self.assertTrue(user.username.startswith("admin_"))

        # Check membership
        membership = GroupMembership.objects.get(user=user, group_id=group_id)
        self.assertEqual(membership.role, 'admin')

    def test_create_group_with_missing_data(self):
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
