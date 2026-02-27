from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model."""

    owner_id = serializers.IntegerField(source='owner.id', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'created_at',
            'updated_at',
            'owner_id',
        ]
        read_only_fields = ['id', 'owner_id', 'created_at', 'updated_at']

    def validate_title(self, value):
        """Validate and strip whitespace from title."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be blank.")
        return value

    def validate_status(self, value):
        """Validate status is one of allowed values."""
        valid_statuses = [choice[0] for choice in Task.Status.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Status must be one of: {', '.join(valid_statuses)}"
            )
        return value

    def validate_priority(self, value):
        """Validate priority is one of allowed values."""
        valid_priorities = [choice[0] for choice in Task.Priority.choices]
        if value not in valid_priorities:
            raise serializers.ValidationError(
                f"Priority must be one of: {', '.join(valid_priorities)}"
            )
        return value