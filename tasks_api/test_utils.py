from typing import Any, Dict
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient

from tasks.models import TaskTemplate
from users.service import register_admin_and_create_group


def setup_admin_user(client: APIClient, username: str = "admin") -> Dict[str, Any]:
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


def create_task_template(client: APIClient) -> Response:
    url = reverse("tasks:create-task")  # or your actual endpoint
    data = {
        "title": "Clean Room",
        "description": "Do it",
        "credits": 100,
        "priority": 1,
    }
    return client.post(url, data, format="json")
