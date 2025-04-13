from typing import Any, Dict, cast
from amqp import NotFound
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from tasks.models import TaskInstance, TaskTemplate
from users.models import Group
from users.service import register_admin_and_create_group
from tasks.service import create_task_instance


def setup_mock_admin_user(client: APIClient, username: str = "admin") -> Dict[str, Any]:
    result = register_admin_and_create_group(username)

    access_token = result["access"]
    group_id = result["group_id"]
    password = result["password"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    return {
        "username": username,
        "access_token": access_token,
        "group_id": group_id,
        "password": password,
    }


def create_mock_task_template(client: APIClient) -> Response:
    url = reverse("tasks:create-task")  # or your actual endpoint
    data = {
        "title": "Clean Room",
        "description": "Do it",
        "credits": 100,
        "priority": 1,
    }
    return client.post(url, data, format="json")


def create_mock_task_instance(
) -> TaskInstance | None:
    task_template = TaskTemplate.objects.first()

    if not task_template:
        raise NotFound("TaskTemplate does not exist")

    create_task_instance(task_template.id)  # type: ignore
    return TaskInstance.objects.first()


def get_mock_invite_link(client: APIClient) -> str:
    group = Group.objects.first()

    if not group:
        raise NotFound("Group does not exist")

    url = reverse('users:invite-url')
    data = {
        'group_id': str(group.id),
        'name': 'Test User',
    }
    res = client.post(url, data, format='json')
    return res.data.get('invite_url')  # type: ignore


def accept_mock_invite(client: APIClient) -> None:
    # First, get the invite link
    invite_url = get_mock_invite_link(client)

    if not invite_url:
        raise NotFound("Invite URL does not exist")

    token = invite_url.split('=')[1]
    url = reverse('users:accept-invite')
    client.post(url, {'token': token}, format='json')


def fake_assign_task_to_user(
    client: APIClient,
    task_instance_id: int,
    user_id: int
) -> Dict[str, Any]:
    url = reverse(
        'tasks:assign-task',
        kwargs={'task_instance_id': task_instance_id,
                'user_id': user_id},
    )

    res = client.put(url, format='json')
    return cast(Dict[str, Any], res.data)
