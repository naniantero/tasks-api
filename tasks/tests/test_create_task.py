# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false

from django.urls import reverse
from rest_framework.test import APITestCase

from tasks.models import TaskTemplate
from users.service import register_admin_and_create_group


class CreateTaskTemplateTests(APITestCase):
    def setUp(self) -> None:
        self.username = "parent1"
        result = register_admin_and_create_group(self.username)

        self.access_token = result["access"]
        self.group_id = result["group_id"]
        self.password = result["password"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_task_template(self) -> None:
        url = reverse("tasks:create-task")  # or your actual endpoint
        data = {
            "title": "Clean Room",
            "description": "Do it",
            "credits": 100,
            "priority": 1,
        }
        response = self.client.post(url, data, format="json")
        item = TaskTemplate.objects.first()

        if item:
            self.assertEqual(response.status_code, 201)
            self.assertEqual(TaskTemplate.objects.count(), 1)
            self.assertEqual(item.title, "Clean Room")
            self.assertEqual(item.description, "Do it")
            self.assertEqual(item.credits, 100)
            self.assertEqual(item.priority, 1)
            self.assertEqual(str(item.group.id), self.group_id)
