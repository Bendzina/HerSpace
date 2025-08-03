from rest_framework import serializers
from .models import WisdomMessage, UserWisdomDelivery, UserProfile, RitualUsage

class WisdomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WisdomMessage
        fields = '__all__'

class UserWisdomDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWisdomDelivery
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['current_mood_context', 'preferred_support_style', 'life_roles', 'created_at', 'updated_at'] 

class RitualUsageSerializer(serializers.ModelSerializer):
    ritual_title = serializers.CharField(source='ritual.title', read_only=True)
    
    class Meta:
        model = RitualUsage
        fields = [
            'id', 'ritual', 'ritual_title', 'used_at', 'was_helpful', 
            'effectiveness_rating', 'mood_before', 'mood_after', 'notes'
        ]
        read_only_fields = ['id', 'used_at', 'ritual_title'] 