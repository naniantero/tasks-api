# pyright: reportUnknownVariableType=false
# pyright: reportUnknownMemberType=false
from django.db import models
from django.conf import settings


class RewardTemplate(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=0)
    priority = models.PositiveIntegerField(default=0)
    group = models.ForeignKey(
        'users.Group', on_delete=models.CASCADE, related_name='reward_templates')

    def __str__(self) -> str:
        return self.title


class RewardInstance(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(
        RewardTemplate, on_delete=models.CASCADE, related_name='instances')
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reward_instances')
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('redeemed', 'Redeemed')
        ],
        default='pending'
    )

    def __str__(self) -> str:
        return f"{self.template.title} for {self.assignee.email or self.assignee.username} on {self.date}"
