from rest_framework import serializers
from .models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(source='get_action_display', read_only=True)

    class Meta:
        model = ActivityLog
        fields = (
            'id', 'actor_display', 'action', 'action_display', 'model_name',
            'object_id', 'object_repr', 'changes', 'created_at',
        )
