# users/tests/test_register_admin.py
# pyright: reportAttributeAccessIssue=false

from django.urls import reverse
from rest_framework.test import APITestCase

from tasks_api.test_utils import get_mock_invite_link, setup_mock_admin_user
from users.models import Group


class InviteUserToGroupTests(APITestCase):
    invite_url = None

    def setUp(self) -> None:
        setup_mock_admin_user(self.client, username="parent1")

    def test_get_invite_link(self) -> None:
        url = get_mock_invite_link(self.client)
        self.assertTrue(url.startswith('/users/group/accept-invite?token='))
        self.invite_url = url

    def test_invite_user_to_group(self) -> None:
        # First, get the invite link
        self.test_get_invite_link()

        if not self.invite_url:
            self.fail("Invite URL not generated")

        token = self.invite_url.split('=')[1]
        url = reverse('users:accept-invite')
        self.client.post(url, {'token': token}, format='json')
        group = Group.objects.first()

        if not group:
            self.fail("Group does not exist")

        group_membership = group.memberships.filter(role='member').first()

        if not group_membership:
            self.fail("Group membership does not exist")

        self.assertEqual(group_membership.role, 'member')
        self.assertEqual(group_membership.user.username, 'Test User')
