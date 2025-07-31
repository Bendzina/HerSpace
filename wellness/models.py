from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WisdomMessage(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField(help_text="Main wisdom message")
    affirmation = models.CharField(max_length=500, blank=True)
    # Personalization Fields
    for_mood_context = models.CharField(
        max_length=50,
        choices=[
            ('any', 'Any Context'),
            ('transition', 'Life Transition'),
            ('motherhood', 'Motherhood'),
            ('career_focus', 'Career Focus'),
            ('healing', 'Healing'),
            ('growth', 'Personal Growth'),
        ],
        default='any'
    )
    for_support_style = models.CharField(
        max_length=30,
        choices=[
            ('any', 'Any Style'),
            ('gentle', 'Gentle'),
            ('empowering', 'Empowering'),
            ('practical', 'Practical'),
            ('spiritual', 'Spiritual'),
        ],
        default='any'
    )
    for_energy_level = models.CharField(
        max_length=20,
        choices=[
            ('any', 'Any Energy Level'),
            ('low', 'Low Energy (1-2)'),
            ('moderate', 'Moderate Energy (3)'),
            ('high', 'High Energy (4-5)'),
        ],
        default='any'
    )
    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UserWisdomDelivery(models.Model):
    """Track which wisdom messages were delivered to users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    wisdom_message = models.ForeignKey(WisdomMessage, on_delete=models.CASCADE)
    delivered_at = models.DateTimeField(auto_now_add=True)
    was_helpful = models.BooleanField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'wisdom_message', 'delivered_at']
