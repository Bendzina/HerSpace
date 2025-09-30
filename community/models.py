from django.db import models
from django.conf import settings

class CommunityPost(models.Model):
    """Anonymous community posts for sharing and support"""
    POST_TYPE_CHOICES = [
        ('support', 'Support Request'),
        ('celebration', 'Celebration'),
        ('advice', 'Advice Seeking'),
        ('story', 'Personal Story'),
        ('question', 'Question'),
        ('gratitude', 'Gratitude'),
    ]
    
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.post_type}: {self.title[:50]}"

class CommunityComment(models.Model):
    """Comments on community posts"""
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment on {self.post.title[:30]}"

class CommunityReaction(models.Model):
    """Reactions to community posts (Facebook-style)"""
    REACTION_CHOICES = [
        ('heart', '❤️ Heart'),
        ('support', '🤗 Support'),
        ('prayer', '🙏 Prayer'),
        ('celebration', '🎉 Celebration'),
        ('hug', '🤗 Hug'),
    ]
    
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='reactions')
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # For anonymous users: track by session_id
    session_id = models.CharField(max_length=255, null=True, blank=True)
    
    # For authenticated users
    is_anonymous = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        # Ensure one reaction per user/session per post
        constraints = [
            models.UniqueConstraint(
                fields=['post', 'user'],
                condition=models.Q(user__isnull=False),
                name='unique_user_reaction_per_post'
            ),
            models.UniqueConstraint(
                fields=['post', 'session_id'],
                condition=models.Q(session_id__isnull=False),
                name='unique_session_reaction_per_post'
            )
        ]
    
    def __str__(self):
        return f"{self.reaction_type} on {self.post.title[:30]}"