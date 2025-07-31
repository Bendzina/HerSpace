from django.urls import path
from .views import (
    CommunityPostListCreateView, CommunityPostDetailView,
    CommunityCommentListCreateView, CommunityReactionCreateView,
    CommunityReactionListView
)

urlpatterns = [
    # Community Posts
    path('posts/', CommunityPostListCreateView.as_view(), name='community-post-list-create'),
    path('posts/<int:pk>/', CommunityPostDetailView.as_view(), name='community-post-detail'),
    
    # Comments
    path('posts/<int:post_id>/comments/', CommunityCommentListCreateView.as_view(), name='community-comment-list-create'),
    
    # Reactions
    path('posts/<int:post_id>/reactions/', CommunityReactionCreateView.as_view(), name='community-reaction-create'),
    path('posts/<int:post_id>/reactions/list/', CommunityReactionListView.as_view(), name='community-reaction-list'),
] 