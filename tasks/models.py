# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false

from django.db import models
from django.conf import settings  # <- This is the correct way to get custom User
# No need to import User directly


class TaskTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=0)
    priority = models.PositiveIntegerField(default=0)
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_instances')
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('completed', 'Completed'),
            ('expired', 'Expired')
        ],
        default='pending'
    )

    def __str__(self):
        return f"{self.template.title} for {self.assignee.username} on {self.date}"
