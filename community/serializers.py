from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CommunityPost, CommunityComment, CommunityReaction

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """მომხმარებლის ინფორმაცია (სახელი, email)"""
    name = serializers.CharField(source='username', read_only=True)  # Use username as name

    class Meta:
        model = User
        fields = ['id', 'name', 'email']
        read_only_fields = ['id']

class CommunityPostSerializer(serializers.ModelSerializer):
    """პოსტის სრული ინფორმაცია + რეაქციები"""
    user = UserSerializer(read_only=True)
    comment_count = serializers.SerializerMethodField()
    reaction_count = serializers.SerializerMethodField()
    user_reactions = serializers.SerializerMethodField()
    
    class Meta:
        model = CommunityPost
        fields = [
            'id', 'post_type', 'title', 'content', 'is_anonymous',
            'created_at', 'updated_at', 'comment_count', 'reaction_count',
            'user_reactions', 'user'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'comment_count', 
            'reaction_count', 'user_reactions', 'user'
        ]
    
    def get_comment_count(self, obj):
        return obj.comments.count()
    
    def get_reaction_count(self, obj):
        return obj.reactions.count()
    
    def get_user_reactions(self, obj):
        """
        დააბრუნებს მიმდინარე იუზერის რეაქციას (მხოლოდ 1!)
        - ავტორიზებულისთვის: user-ით
        - ანონიმურისთვის: session_id-ით
        """
        request = self.context.get('request')
        if not request:
            return []
        
        # ავტორიზებული იუზერი
        if request.user.is_authenticated:
            reaction = CommunityReaction.objects.filter(
                post=obj,
                user=request.user
            ).first()
            return [reaction.reaction_type] if reaction else []
        
        # ანონიმური იუზერი (session_id)
        session_id = request.session.session_key
        if not session_id:
            # თუ session არ არსებობს, შექმენი
            request.session.create()
            session_id = request.session.session_key
        
        if session_id:
            reaction = CommunityReaction.objects.filter(
                post=obj,
                session_id=session_id,
                user=None
            ).first()
            return [reaction.reaction_type] if reaction else []
        
        return []

class CommunityPostCreateSerializer(serializers.ModelSerializer):
    """პოსტის შექმნა"""
    class Meta:
        model = CommunityPost
        fields = ['post_type', 'title', 'content', 'is_anonymous']
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated and not validated_data.get('is_anonymous', True):
            validated_data['user'] = request.user
        return super().create(validated_data)

class CommunityCommentSerializer(serializers.ModelSerializer):
    """კომენტარის სრული ინფორმაცია"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CommunityComment
        fields = ['id', 'content', 'is_anonymous', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']

class CommunityCommentCreateSerializer(serializers.ModelSerializer):
    """კომენტარის შექმნა"""
    class Meta:
        model = CommunityComment
        fields = ['content', 'is_anonymous']

    def create(self, validated_data):
        # post_id will be passed via context or perform_create
        post_id = self.context.get('post_id')
        if post_id:
            validated_data['post_id'] = post_id

        request = self.context.get('request')
        if request and request.user.is_authenticated and not validated_data.get('is_anonymous', True):
            validated_data['user'] = request.user
        return super().create(validated_data)

class CommunityReactionSerializer(serializers.ModelSerializer):
    """რეაქციის ინფორმაცია"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CommunityReaction
        fields = ['id', 'reaction_type', 'is_anonymous', 'created_at', 'user']
        read_only_fields = ['id', 'created_at', 'user']