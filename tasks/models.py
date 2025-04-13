# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false

from django.conf import settings
from django.db import models
from django.utils.timezone import now


class TaskStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    COMPLETED = 'completed', 'Completed'
    EXPIRED = 'expired', 'Expired',
    PENDING_REVIEW = 'pending_review', 'Pending Review'


class TaskTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=0)
    priority = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(default=now)
    interval = models.CharField(
        max_length=10, default='daily')  # daily, weekly, custom
    daily_quota = models.PositiveIntegerField(default=0)
    group = models.ForeignKey(
        'users.Group', on_delete=models.CASCADE, related_name='task_templates')

    def __str__(self) -> str:
        return self.title


class TaskInstance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(
        TaskTemplate, on_delete=models.CASCADE, related_name='instances')
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_instances',    null=True,
        blank=True)
    status = models.CharField(
        max_length=32,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING,
    )

    def __str__(self) -> str:
        return f"{self.template.title}: Created: {self.created_at}, Status: {self.status}. Template ID: {self.template.id}"
