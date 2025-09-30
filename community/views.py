from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import CommunityPost, CommunityComment, CommunityReaction
from .serializers import (
    CommunityPostSerializer, CommunityPostCreateSerializer,
    CommunityCommentSerializer, CommunityCommentCreateSerializer,
    CommunityReactionSerializer
)

class CommunityPostListCreateView(generics.ListCreateAPIView):
    """List and create community posts"""
    permission_classes = [AllowAny]
    filterset_fields = ['post_type', 'is_anonymous', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'comment_count', 'reaction_count']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    
    def get_queryset(self):
        return CommunityPost.objects.filter(is_approved=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityPostCreateSerializer
        return CommunityPostSerializer
    
    def perform_create(self, serializer):
        if self.request.user.is_authenticated and not serializer.validated_data.get('is_anonymous', True):
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class CommunityPostDetailView(generics.RetrieveAPIView):
    """Get a specific community post"""
    permission_classes = [AllowAny]
    serializer_class = CommunityPostSerializer
    
    def get_queryset(self):
        return CommunityPost.objects.filter(is_approved=True)

class CommunityCommentListCreateView(generics.ListCreateAPIView):
    """List and create comments for a post"""
    permission_classes = [AllowAny]
    serializer_class = CommunityCommentSerializer
    filterset_fields = ['is_anonymous', 'created_at']
    ordering_fields = ['created_at']
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return CommunityComment.objects.filter(post_id=post_id)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommunityCommentCreateSerializer
        return CommunityCommentSerializer
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        # Pass post_id through context
        serializer.context['post_id'] = post_id
        serializer.save()

class CommunityReactionCreateView(generics.CreateAPIView):
    """Add/remove/change reaction to a post (Facebook-style)"""
    permission_classes = [AllowAny]
    serializer_class = CommunityReactionSerializer
    
    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        reaction_type = request.data.get('reaction_type')
        is_anonymous = request.data.get('is_anonymous', True)
        
        # Get user identifier (session_id for anonymous, user for authenticated)
        if request.user.is_authenticated and not is_anonymous:
            user_filter = {'user': request.user}
            create_data = {'user': request.user, 'is_anonymous': False}
        else:
            # For anonymous users, use session_id to track reactions
            session_id = request.session.session_key
            if not session_id:
                request.session.create()
                session_id = request.session.session_key
            user_filter = {'session_id': session_id, 'user': None}
            create_data = {'session_id': session_id, 'is_anonymous': True}
        
        # Check if user already has ANY reaction on this post
        existing_reaction = CommunityReaction.objects.filter(
            post_id=post_id,
            **user_filter
        ).first()
        
        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # Toggle off: remove the same reaction
                existing_reaction.delete()
                return Response(
                    {"message": "Reaction removed", "action": "removed"},
                    status=status.HTTP_200_OK
                )
            else:
                # Change reaction: update to new type
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
                serializer = self.get_serializer(existing_reaction)
                return Response(
                    {**serializer.data, "action": "changed"},
                    status=status.HTTP_200_OK
                )
        else:
            # Add new reaction
            reaction = CommunityReaction.objects.create(
                post_id=post_id,
                reaction_type=reaction_type,
                **create_data
            )
            serializer = self.get_serializer(reaction)
            return Response(
                {**serializer.data, "action": "added"},
                status=status.HTTP_201_CREATED
            )

class CommunityReactionListView(generics.ListAPIView):
    """List reactions for a post"""
    permission_classes = [AllowAny]
    serializer_class = CommunityReactionSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return CommunityReaction.objects.filter(post_id=post_id)