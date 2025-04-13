from rest_framework import serializers

from rewards.models import RewardTemplate


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardTemplate
        fields = ['title']

    def validate_name(self, value: str) -> str:
        if not value.strip():
            raise serializers.ValidationError("reward name cannot be empty.")
        if RewardTemplate.objects.filter(title=value).exists():
            raise serializers.ValidationError("reward already exists.")
        return value
