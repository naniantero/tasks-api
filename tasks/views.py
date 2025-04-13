from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.serializers import TaskInstanceSerializer, TaskTemplateSerializer
from tasks.service import assign_task_instance_to_user, create_task_template


class CreateTaskTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        """
        Create a new task template.
        The request body should contain the task template data.
        """
        task = create_task_template(request)
        return Response(TaskTemplateSerializer(task).data, status=201)


class AssignTaskView(APIView):

    def post(self, request: Request) -> Response:
        """
        Assign a task instance to a user.
        The request body should contain the task instance ID and user ID.
        """
        try:
            task_instance = assign_task_instance_to_user(request)
            return Response(TaskInstanceSerializer(task_instance).data, status=204)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
