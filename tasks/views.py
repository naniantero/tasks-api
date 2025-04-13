from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.serializers import TaskInstanceSerializer, TaskTemplateSerializer
from tasks.service import (assign_task_instance_to_user, create_task_template,
                           set_task_instance_completed,
                           set_task_instance_for_review)


class CreateTaskTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Create a new task template.
        The request args should contain the task template data.
        """
        task = create_task_template(request)
        return Response(TaskTemplateSerializer(task).data, status=201)


class AssignTaskView(APIView):

    def put(self, _request: Request, task_instance_id: int, user_id: int) -> Response:
        """
        Assign a task instance to a user.
        The request args should contain the task instance ID and user ID.
        """
        task_instance = assign_task_instance_to_user(
            task_instance_id, user_id)
        return Response(TaskInstanceSerializer(task_instance).data, status=200)


class SetTaskForReviewView(APIView):
    def put(self, _request: Request, task_instance_id: int, user_id: int) -> Response:
        """
        Sets a task instance for review.
        """
        task_instance = set_task_instance_for_review(
            task_instance_id, user_id)
        return Response(TaskInstanceSerializer(task_instance).data, status=200)


class SetTaskCompletedView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, _request: Request, task_instance_id: int) -> Response:
        """
        Sets a task instance completed (By admin)
        """
        task_instance = set_task_instance_completed(
            task_instance_id)
        return Response(TaskInstanceSerializer(task_instance).data, status=200)
