# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false

from rest_framework.test import APITestCase

from tasks.models import TaskStatus
from tasks_api.test_utils import (create_mock_task_instance,
                                  create_mock_task_template,
                                  setup_mock_admin_user)


class CreateTaskInstanceTests(APITestCase):
    def setUp(self) -> None:
        setup_mock_admin_user(self.client, username="parent1")
        create_mock_task_template(self.client)

    def test_create_task_instance(self) -> None:
        task_instance = create_mock_task_instance()

        if task_instance:
            self.assertIsNotNone(
                task_instance, "TaskInstance should exist at this point")
            self.assertEqual(task_instance.status, TaskStatus.PENDING)
            self.assertEqual(task_instance.template.credits, 100)
        else:
            self.fail("TaskInstance was not created")
