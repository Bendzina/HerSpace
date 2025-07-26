from rest_framework import serializers
from .models import ChildcareRoutine, MotherhoodResource, MotherhoodJournal, SupportGroup

class ChildcareRoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildcareRoutine
        fields = ['id', 'title', 'routine_type', 'description', 'time_of_day', 'duration_minutes', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class MotherhoodResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherhoodResource
        fields = ['id', 'title', 'resource_type', 'category', 'description', 'url', 'author', 'is_featured', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

class MotherhoodJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotherhoodJournal
        fields = ['id', 'title', 'content', 'mood', 'is_private', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class SupportGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportGroup
        fields = ['id', 'name', 'group_type', 'description', 'is_private', 'max_members', 'current_members', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at'] 