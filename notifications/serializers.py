from rest_framework import serializers
from .models import Notification, NotificationPreference, NotificationTemplate

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message', 'priority',
            'is_read', 'is_sent', 'created_at', 'scheduled_for'
        ]
        read_only_fields = ['id', 'created_at', 'is_sent']

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = [
            'id', 'mood_reminder_enabled', 'mood_reminder_time', 'mood_reminder_days',
            'task_reminder_enabled', 'task_reminder_time',
            'journal_reminder_enabled', 'journal_reminder_time',
            'community_notifications_enabled', 'comment_notifications_enabled',
            'reaction_notifications_enabled', 'insight_notifications_enabled',
            'weekly_insight_enabled', 'email_notifications_enabled',
            'push_notifications_enabled', 'quiet_hours_start', 'quiet_hours_end',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'template_type', 'title_template', 'message_template', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class NotificationMarkReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of notification IDs to mark as read"
    )

class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['notification_type', 'title', 'message', 'priority', 'scheduled_for']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data) 