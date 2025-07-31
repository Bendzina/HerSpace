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
    
    # Anonymous posting - no user field
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_anonymous = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=True)  # For moderation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Optional user field for non-anonymous posts
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
    
    # Optional user field for non-anonymous comments
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
    """Reactions to community posts (hearts, support, etc.)"""
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
    
    # Anonymous reactions
    is_anonymous = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    class Meta:
        unique_together = ['post', 'reaction_type', 'user']  # One reaction per type per user
    
    def __str__(self):
        return f"{self.reaction_type} on {self.post.title[:30]}"
