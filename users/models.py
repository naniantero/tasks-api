from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class GroupMembership(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self) -> str:
        return f"{self.user.username} in {self.group.name} as {self.role}"


class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True) # type: ignore
    credits = models.PositiveIntegerField(default=0)
    device_id = models.CharField(
        max_length=100, blank=True, null=True, unique=True)

    USERNAME_FIELD = 'username'

    def __str__(self) -> str:
        return self.email or self.username
