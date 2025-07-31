from rest_framework import serializers
from .models import CommunityPost, CommunityComment, CommunityReaction

class CommunityPostSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    user_reactions = serializers.SerializerMethodField()
    
    class Meta:
        model = CommunityPost
        fields = [
            'id', 'post_type', 'title', 'content', 'is_anonymous',
            'created_at', 'updated_at', 'comment_count', 'reaction_count',
            'user_reactions'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'comment_count', 'reaction_count', 'user_reactions']
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_reaction_count(self, obj):
        return obj.reactions.count()
    
    def get_user_reactions(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_reactions = obj.reactions.filter(user=request.user)
            return [reaction.reaction_type for reaction in user_reactions]
        return []

class CommunityCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = ['id', 'content', 'is_anonymous', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommunityReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityReaction
        fields = ['id', 'reaction_type', 'is_anonymous', 'created_at']
        read_only_fields = ['id', 'created_at']

class CommunityPostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = ['post_type', 'title', 'content', 'is_anonymous']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated and not validated_data.get('is_anonymous', True):
            validated_data['user'] = request.user
        return super().create(validated_data)

class CommunityCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityComment
        fields = ['content', 'is_anonymous']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated and not validated_data.get('is_anonymous', True):
            validated_data['user'] = request.user
        return super().create(validated_data) 