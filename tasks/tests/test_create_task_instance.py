# pyright: reportAttributeAccessIssue=false
# pyright: reportOptionalMemberAccess=false

from rest_framework.test import APITestCase

from tasks.models import TaskInstance, TaskTemplate
from tasks.service import create_task_instance
from tasks_api.test_utils import create_task_template, setup_admin_user


class CreateTaskTemplateTests(APITestCase):
    def setUp(self) -> None:
        setup_admin_user(self.client, username="parent1")
        create_task_template(self.client)

    def test_create_task_instance(self) -> None:
        task_template = TaskTemplate.objects.first()
        self.assertIsNotNone(
            task_template, "TaskTemplate should exist at this point")

        if not task_template:
            self.fail("TaskTemplate was not created")
            
        create_task_instance(task_template.id)
        task_instance = TaskInstance.objects.first()

        if task_instance:
            self.assertIsNotNone(
                task_instance, "TaskInstance should exist at this point")
            self.assertEqual(task_instance.template, task_template)
            self.assertEqual(task_instance.status, "pending")
            self.assertEqual(task_instance.template.credits, 100)
        else:
            self.fail("TaskInstance was not created")
