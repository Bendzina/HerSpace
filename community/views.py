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
    permission_classes = [AllowAny]  # Allow anonymous viewing
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
        if self.request.user.is_authenticated and not serializer.validated_data.get('is_anonymous', True):
            serializer.save(post_id=post_id, user=self.request.user)
        else:
            serializer.save(post_id=post_id)

class CommunityReactionCreateView(generics.CreateAPIView):
    """Add a reaction to a post"""
    permission_classes = [AllowAny]
    serializer_class = CommunityReactionSerializer
    
    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        reaction_type = serializer.validated_data['reaction_type']
        
        # Check if user already reacted with this type
        existing_reaction = CommunityReaction.objects.filter(
            post_id=post_id,
            reaction_type=reaction_type,
            user=self.request.user if self.request.user.is_authenticated else None
        ).first()
        
        if existing_reaction:
            # Remove existing reaction (toggle off)
            existing_reaction.delete()
            return Response({"message": "Reaction removed"}, status=status.HTTP_200_OK)
        else:
            # Add new reaction
            if self.request.user.is_authenticated and not serializer.validated_data.get('is_anonymous', True):
                serializer.save(post_id=post_id, user=self.request.user)
            else:
                serializer.save(post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class CommunityReactionListView(generics.ListAPIView):
    """List reactions for a post"""
    permission_classes = [AllowAny]
    serializer_class = CommunityReactionSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return CommunityReaction.objects.filter(post_id=post_id)
