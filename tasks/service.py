# pyright: reportAttributeAccessIssue=false

from typing import Any, Dict, cast

from amqp import NotFound
from rest_framework.request import Request

from tasks.serializers import TaskTemplateSerializer
from users.models import Group
from users.service import deposit_credits, get_user_by_id

from .models import TaskInstance, TaskStatus, TaskTemplate


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
        raise NotFound("Template not found")

    task = TaskInstance.objects.create(
        template=template
    )

    return task


def assign_task_instance_to_user(task_instance_id: int, user_id: int) -> None | TaskInstance:
    _validate_task_user_ids(task_instance_id, user_id)
    task_instance = get_instance_by_id(task_instance_id)
    user = get_user_by_id(user_id)

    task_instance.assignee = user
    task_instance.save()

    return TaskInstance.objects.get(id=task_instance_id)


def set_task_instance_for_review(task_instance_id: int, user_id: int) -> None | TaskInstance:
    _validate_task_user_ids(task_instance_id, user_id)
    task_instance = get_instance_by_id(task_instance_id)
    user = get_user_by_id(user_id)

    if task_instance.assignee != user:
        raise PermissionError("User is not the assignee of this task instance")

    task_instance.assignee = user
    task_instance.status = TaskStatus.PENDING_REVIEW
    task_instance.save()

    return TaskInstance.objects.get(id=task_instance_id)


def set_task_instance_completed(task_instance_id: int) -> None | TaskInstance:
    task_instance = get_instance_by_id(task_instance_id)

    if task_instance.status != TaskStatus.PENDING_REVIEW:
        raise PermissionError("Task instance is not in review status")

    task_instance.status = TaskStatus.COMPLETED
    task_instance.save()

    if not task_instance.assignee:
        raise ValueError("Task instance has no assignee")

    # Deposit credits to the user who completed the task
    deposit_credits(task_instance.assignee.id, task_instance.template.credits)

    return TaskInstance.objects.get(id=task_instance_id)


def get_instance_by_id(task_instance_id: int) -> TaskInstance:
    task_instance = TaskInstance.objects.get(id=task_instance_id)
    if not task_instance:
        raise NotFound("Task instance not found")

    return task_instance


def _validate_task_user_ids(task_instance_id: int, user_id: int) -> None:
    if not task_instance_id or not user_id:
        raise ValueError("Task instance ID and user ID are required")
