from rest_framework import serializers
from .models import (
    WisdomMessage, 
    UserWisdomDelivery, 
    UserProfile, 
    RitualUsage,
    MindfulnessActivity,
    MindfulnessSession
)

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


class MindfulnessActivitySerializer(serializers.ModelSerializer):
    """Serializer for MindfulnessActivity model"""
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    audio_file = serializers.SerializerMethodField()
    
    def get_audio_file(self, obj):
        try:
            print(f"\n=== DEBUG: get_audio_file for activity {getattr(obj, 'id', 'unknown')} ===")
            
            if not obj.audio_file:
                print("❌ No audio file field found on the object")
                return None
                
            print(f"📁 Audio file field value: {obj.audio_file}")
            print(f"📂 Storage class: {obj.audio_file.storage.__class__.__name__}")
            
            # Check if the file exists in storage
            try:
                file_exists = obj.audio_file.storage.exists(obj.audio_file.name)
                print(f"✅ File exists in storage: {file_exists}")
                if not file_exists:
                    print(f"⚠️  File not found at: {obj.audio_file.path}")
                    return None
            except Exception as storage_error:
                print(f"⚠️  Error checking file existence: {str(storage_error)}")
            
            # Get the request from context for building absolute URLs
            request = self.context.get('request')
            if request is None:
                print("⚠️  No request in context, returning relative URL")
                return obj.audio_file.url
            
            # Try to build absolute URL
            try:
                relative_url = obj.audio_file.url
                print(f"🔗 Relative URL: {relative_url}")
                
                # Ensure the URL is properly encoded
                from urllib.parse import quote
                encoded_url = quote(relative_url, safe=':/?=&')
                
                # Build absolute URL
                absolute_url = request.build_absolute_uri(encoded_url)
                print(f"🌐 Absolute URL: {absolute_url}")
                
                # If running on local network, make sure we're using the correct host
                if '127.0.0.1' in absolute_url or 'localhost' in absolute_url:
                    print("⚠️  Warning: Using localhost URL - may not be accessible from device")
                    print("   Try accessing this URL from your device's browser to test:", absolute_url)
                
                return absolute_url
                
            except Exception as url_error:
                print(f"❌ Error building URL: {str(url_error)}")
                print("🔄 Falling back to relative URL")
                return obj.audio_file.url
                
        except Exception as e:
            # Log the full error but don't fail the entire request
            import traceback
            error_trace = traceback.format_exc()
            print(f"❌❌❌ CRITICAL ERROR in get_audio_file for activity {getattr(obj, 'id', 'unknown')}")
            print(f"Error: {str(e)}")
            print("Stack trace:")
            print(error_trace)
            return None
    
    class Meta:
        model = MindfulnessActivity
        fields = [
            'id', 'title', 'description', 'short_description', 'icon',
            'duration_minutes', 'audio_file', 'image', 'category', 'category_display',
            'difficulty', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'category_display']
    
    def get_title(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'en') if request else 'en'
        return obj.get_title(language)
    
    def get_description(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'en') if request else 'en'
        return obj.get_description(language)
    
    def get_short_description(self, obj):
        request = self.context.get('request')
        language = request.query_params.get('lang', 'en') if request else 'en'
        return obj.get_short_description(language)


class MindfulnessSessionSerializer(serializers.ModelSerializer):
    """Serializer for MindfulnessSession model"""
    activity_title = serializers.CharField(source='activity.title', read_only=True)
    
    class Meta:
        model = MindfulnessSession
        fields = [
            'id', 'activity', 'activity_title', 'started_at', 'duration_minutes',
            'mood_before', 'mood_after', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at'] 