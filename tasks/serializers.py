from rest_framework import serializers

from tasks.models import TaskTemplate


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ['name']

    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("task name cannot be empty.")
        if TaskTemplate.objects.filter(name=value).exists():
            raise serializers.ValidationError("task already exists.")
        return value
