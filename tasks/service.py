# pyright: reportAttributeAccessIssue=false

from typing import Any, Dict, cast

from rest_framework.request import Request

from tasks.serializers import AssignTaskSerializer, TaskTemplateSerializer
from users.models import Group, User

from .models import TaskInstance, TaskTemplate


def create_task_template(request: Request) -> TaskTemplate:
    group_id = request.auth.get("group_id")  # type: ignore
    serializer = TaskTemplateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    group = Group.objects.get(id=group_id)
    data = cast(Dict[str, Any], serializer.validated_data)

    task = TaskTemplate.objects.create(
        **data,
        group=group
    )

    return task


def create_task_instance(template_id: int) -> TaskInstance:
    template = TaskTemplate.objects.get(id=template_id)

    if not template:
        raise ValueError("Template not found")

    task = TaskInstance.objects.create(
        template=template
    )

    return task


def assign_task_instance_to_user(request: Request) -> None | TaskInstance:
    serializer = AssignTaskSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = cast(Dict[str, Any], serializer.validated_data)

    task_instance_id = data.get("task_instance_id")
    user_id = data.get("user_id")

    if not task_instance_id or not user_id:
        raise ValueError("Task instance ID and user ID are required")

    task_instance = TaskInstance.objects.get(id=task_instance_id)
    if not task_instance:
        raise ValueError("Task instance not found")

    user = User.objects.get(id=user_id)
    if not user:
        raise ValueError("User not found")

    task_instance.assignee = user
    task_instance.save()

    return TaskInstance.objects.get(id=task_instance_id)
