from rest_framework import serializers
from .models import JournalEntry, MoodCheckIn, DailyTask, Ritual, TarotCard, TarotPrompt, TarotDeck, AIConversation

class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = JournalEntry
        fields = ['id', 'created_at', 'title', 'content']  # include title
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'title': {'required': False, 'allow_blank': True},
            'content': {'required': False, 'allow_blank': True},
        }

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

class TarotCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarotCard
        fields = [
            'id', 'name', 'description', 'image_url', 'is_active',
            'is_major_arcana', 'suit', 'upright_meanings', 'reversed_meanings',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class TarotPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TarotPrompt
        fields = [
            'id', 'prompt_type', 'question', 'cards_drawn', 'interpretation',
            'advice', 'is_ai_generated', 'ai_model_used', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class TarotDeckSerializer(serializers.ModelSerializer):
    cards = TarotCardSerializer(many=True, read_only=True)

    class Meta:
        model = TarotDeck
        fields = ['id', 'name', 'description', 'is_active', 'cards', 'created_at']
        read_only_fields = ['id', 'created_at']

class AIConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIConversation
        fields = [
            'id', 'conversation_type', 'user_message', 'ai_response',
            'context_data', 'is_favorite', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class GPTPromptSerializer(serializers.Serializer):
    prompt = serializers.CharField()