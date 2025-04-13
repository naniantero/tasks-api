from rest_framework import serializers

from tasks.models import TaskTemplate


class TaskTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskTemplate
        fields = ['title', 'description', 'credits', 'priority']

    def validate_title(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("Task template title cannot be empty.")
        if TaskTemplate.objects.filter(title=value).exists():
            raise serializers.ValidationError("Task template already exists.")
        return value
