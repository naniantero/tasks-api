# # pyright: reportAttributeAccessIssue=false
# # pyright: reportOptionalMemberAccess=false

# from django.urls import reverse
# from rest_framework.test import APITestCase

# from tasks.models import TaskTemplate
# from tasks_api.test_utils import create_mock_task_instance, create_mock_task_template, setup_mock_admin_user


# class CreateTaskTemplateTests(APITestCase):
#     task_instance_id = None

#     def setUp(self) -> None:
#         self.admin = setup_mock_admin_user(self.client, username="parent1")
#         create_mock_task_template(self.client)
        
#         # Create a task instance for the test
#         task_instance = create_mock_task_instance()
#         self.task_instance_id = task_instance.id if task_instance else None

#     def test_assign_task_to_user(self) -> None:
#        url = reverse("tasks:assign-task", kwargs={
#             "task_id": self.task_instance_id,
#             "user_id": 
#         })
#         response = self.client.post(url, data, format="json")
#         item = TaskTemplate.objects.first()
#         task_instance = item.task_instances.first() if item else None
#         if task_instance:
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(task_instance.assignee.id, self.admin["group_id"])
#             self.assertEqual(task_instance.status, "assigned")
#             self.assertEqual(task_instance.template.credits, 100)
#             self.assertEqual(task_instance.template.priority, 1)
#         else:
#             self.fail("TaskInstance was not assigned")