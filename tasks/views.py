from urllib.request import Request
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tasks.serializers import TaskSerializer
from tasks.service import create_task


class CreateTaskView(APIView):
    """
    API endpoint to create a new task.
    """

    def post(self, request: Request) -> Response:
        serializer = TaskSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        task_name: str = serializer.validated_data["name"]  # type: ignore
        task = create_task(task_name)
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
