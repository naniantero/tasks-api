# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false

from rest_framework.test import APITestCase

from tasks.models import TaskTemplate
from tasks_api.test_utils import create_task_template, setup_admin_user


class CreateTaskTemplateTests(APITestCase):
    def setUp(self) -> None:
        self.admin = setup_admin_user(self.client, username="parent1")
        self.group_id = self.admin["group_id"]

    def test_create_task_template(self) -> None:
        response = create_task_template(self.client)
        item = TaskTemplate.objects.first()

        if item:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(TaskTemplate.objects.count(), 1)
            self.assertEqual(item.title, "Clean Room")
            self.assertEqual(item.description, "Do it")
            self.assertEqual(item.credits, 100)
            self.assertEqual(item.priority, 1)
            self.assertEqual(str(item.group.id), self.group_id)
        else:
            self.fail("TaskTemplate was not created")
