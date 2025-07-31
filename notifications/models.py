from django.db import models
from django.conf import settings

class Notification(models.Model):
    """User notifications for various events"""
    NOTIFICATION_TYPE_CHOICES = [
        ('mood_reminder', 'Mood Check-in Reminder'),
        ('task_reminder', 'Task Reminder'),
        ('journal_reminder', 'Journal Reminder'),
        ('community_post', 'New Community Post'),
        ('comment_reply', 'Comment Reply'),
        ('reaction_received', 'Reaction Received'),
        ('insight_ready', 'New Insight Available'),
        ('ritual_suggestion', 'Ritual Suggestion'),
        ('custom', 'Custom Notification'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)  # For email/push notifications
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(null=True, blank=True)  # For scheduled notifications
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type}: {self.title}"

class NotificationPreference(models.Model):
    """User preferences for different notification types"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Mood check-in preferences
    mood_reminder_enabled = models.BooleanField(default=True)
    mood_reminder_time = models.TimeField(default='09:00:00')  # Default 9 AM
    mood_reminder_days = models.JSONField(default=list)  # ['monday', 'tuesday', etc.]
    
    # Task reminder preferences
    task_reminder_enabled = models.BooleanField(default=True)
    task_reminder_time = models.TimeField(default='08:00:00')  # Default 8 AM
    
    # Journal reminder preferences
    journal_reminder_enabled = models.BooleanField(default=True)
    journal_reminder_time = models.TimeField(default='20:00:00')  # Default 8 PM
    
    # Community preferences
    community_notifications_enabled = models.BooleanField(default=True)
    comment_notifications_enabled = models.BooleanField(default=True)
    reaction_notifications_enabled = models.BooleanField(default=True)
    
    # Analytics preferences
    insight_notifications_enabled = models.BooleanField(default=True)
    weekly_insight_enabled = models.BooleanField(default=True)
    
    # General preferences
    email_notifications_enabled = models.BooleanField(default=False)
    push_notifications_enabled = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user']
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"

class NotificationTemplate(models.Model):
    """Templates for different types of notifications"""
    TEMPLATE_TYPE_CHOICES = [
        ('mood_reminder', 'Mood Check-in Reminder'),
        ('task_reminder', 'Task Reminder'),
        ('journal_reminder', 'Journal Reminder'),
        ('welcome', 'Welcome Message'),
        ('milestone', 'Milestone Achievement'),
        ('insight', 'Insight Notification'),
        ('ritual_suggestion', 'Ritual Suggestion'),
    ]
    
    template_type = models.CharField(max_length=30, choices=TEMPLATE_TYPE_CHOICES)
    title_template = models.CharField(max_length=255)
    message_template = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['template_type']
    
    def __str__(self):
        return f"{self.template_type} template"
