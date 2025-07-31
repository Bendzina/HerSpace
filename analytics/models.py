from django.db import models
from django.conf import settings

# Create your models here.

class UserInsight(models.Model):
    """Stores computed insights for users"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    insight_type = models.CharField(max_length=50)  # 'mood_pattern', 'task_completion', 'journal_frequency'
    data = models.JSONField()  # Store computed data as JSON
    computed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'insight_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.insight_type}"
