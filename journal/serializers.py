from rest_framework import serializers
from .models import JournalEntry, MoodCheckIn, DailyTask, Ritual

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = '__all__'
class MoodCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCheckIn
        fields = '__all__'

class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTask
        fields = '__all__'

class RitualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ritual
        fields = '__all__'

class GPTPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField()