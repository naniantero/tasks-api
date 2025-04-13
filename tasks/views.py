from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.serializers import TaskTemplateSerializer
from tasks.service import create_task_template


class CreateTaskTemplateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        task = create_task_template(request)
        return Response(TaskTemplateSerializer(task).data, status=201)
