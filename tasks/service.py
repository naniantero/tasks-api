# pyright: reportAttributeAccessIssue=false

from typing import Any, Dict, cast

from rest_framework.request import Request

from tasks.serializers import TaskTemplateSerializer
from users.models import Group

from .models import TaskTemplate


def create_task_template(request: Request) -> TaskTemplate:
    group_id = request.auth.get("group_id") # type: ignore
    serializer = TaskTemplateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    group = Group.objects.get(id=group_id)
    data = cast(Dict[str, Any], serializer.validated_data)

    task = TaskTemplate.objects.create(
        **data,
        group=group
    )

    return task
