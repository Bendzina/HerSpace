from rest_framework import serializers
from .models import UserInsight

class UserInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInsight
        fields = ['id', 'insight_type', 'data', 'computed_at']
        read_only_fields = ['id', 'computed_at']

class MoodAnalyticsSerializer(serializers.Serializer):
    total_checkins = serializers.IntegerField()
    mood_distribution = serializers.DictField()
    most_common_mood = serializers.CharField()
    average_mood_score = serializers.FloatField()
    mood_trend = serializers.ListField()

class TaskAnalyticsSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    task_completion_trend = serializers.ListField()
    most_completed_task_type = serializers.CharField()

class JournalAnalyticsSerializer(serializers.Serializer):
    total_entries = serializers.IntegerField()
    average_entries_per_week = serializers.FloatField()
    most_active_day = serializers.CharField()
    entry_length_stats = serializers.DictField()
    journaling_streak = serializers.IntegerField() 