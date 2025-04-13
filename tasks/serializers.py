from rest_framework import serializers

from tasks.models import TaskInstance, TaskTemplate


class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ['title', 'description', 'credits', 'priority']

    def validate_title(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError(
                "Task template title cannot be empty.")
        if TaskTemplate.objects.filter(title=value).exists():
            raise serializers.ValidationError("Task template already exists.")
        return value


class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = ['template', 'assignee', 'date', 'status']

    def validate_template(self, value: TaskTemplate) -> TaskTemplate:
        if not isinstance(value, TaskTemplate):
            raise serializers.ValidationError("Invalid task template.")
        return value
