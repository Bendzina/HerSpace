from rest_framework import serializers
from .models import JournalEntry, MoodCheckIn, DailyTask, Ritual

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'created_at', 'content']
        read_only_fields = ['id', 'created_at']

class MoodCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCheckIn
        fields = ['id', 'date', 'mood', 'notes']
        read_only_fields = ['id', 'date']

class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = ['id', 'date', 'body_task', 'work_task', 'soul_task', 'completed']
        read_only_fields = ['id', 'date']

class RitualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ritual
        fields = [
            'id', 'title', 'description', 'ritual_type', 'content',
            'for_life_phase', 'emotional_tone', 'duration_minutes',
            'is_for_beginners', 'tags', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class GPTPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField()