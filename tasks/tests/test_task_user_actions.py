# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false
from typing import Any, Dict, cast
from django.urls import reverse
from rest_framework.test import APITestCase

from tasks.models import TaskStatus
from tasks_api.test_utils import (accept_mock_invite, fake_assign_task_to_user,
                                  create_mock_task_instance,
                                  create_mock_task_template,
                                  setup_mock_admin_user)
from users.models import Group
from users.service import get_user_by_id


class TaskUserActions(APITestCase):
    task_instance_id: int | None = None
    user = None

    def setUp(self) -> None:
        """Set up the test case by creating a mock basic user and task instance."""
        self.admin = setup_mock_admin_user(self.client, username="parent1")
        create_mock_task_template(self.client)

        # Create a task instance for the test
        task_instance = create_mock_task_instance()
        self.task_instance_id = task_instance.id if task_instance else None

        accept_mock_invite(self.client)
        group = Group.objects.first()

        if not group:
            self.fail("Group does not exist")

        group_membership = group.memberships.filter(role='member').first()
        self.user = group_membership.user  # type: ignore

    def test_assign_task_to_user(self) -> None:
        if self.task_instance_id is None:
            self.fail("Task instance ID is None")

        data = fake_assign_task_to_user(
            self.client, self.task_instance_id, self.user.id)  # type: ignore

        if not data:
            self.fail("Data is None")

        self.assertIsNotNone(data['template'])
        self.assertEqual(data['assignee'], self.user.id) # type: ignore
        self.assertEqual(data['status'], TaskStatus.PENDING)

    def test_set_task_instance_for_review(self) -> None:
        if self.task_instance_id is None:
            self.fail("Task instance ID is None")
        fake_assign_task_to_user(
            self.client, self.task_instance_id, self.user.id)  # type: ignore
        url = reverse('tasks:set-for-review',
                      kwargs={'task_instance_id': self.task_instance_id, 'user_id': self.user.id}) # type: ignore

        response = self.client.put(url, format='json')
        response_data: Dict[str, Any] = cast(Dict[str, Any], response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], TaskStatus.PENDING_REVIEW)

    def test_set_task_instance_completed(self) -> None:
        self.test_set_task_instance_for_review()
        url = reverse('tasks:set-completed',
                      kwargs={'task_instance_id': self.task_instance_id, })

        response = self.client.put(url, format='json')
        response_data: Dict[str, Any] = cast(Dict[str, Any], response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data['status'], TaskStatus.COMPLETED)

        assignee = get_user_by_id(self.user.id)  # type: ignore
        self.assertEqual(assignee.credits, 100)  # type: ignore
