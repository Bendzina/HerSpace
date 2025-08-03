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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    current_mood_context = models.CharField(
        max_length=50,
        choices=[
            ('transition', 'Life Transition'),
            ('motherhood', 'Motherhood Journey'),
            ('career_focus', 'Career Focus'),
            ('healing', 'Healing Phase'),
            ('growth', 'Personal Growth'),
            ('balance', 'Seeking Balance'),
        ],
        blank=True,
        null=True,
        help_text="What phase of life are you in"
    )
    preferred_support_style = models.CharField(
        max_length=30,
        choices=[
            ('gentle', 'Gentle & Nurturing'),
            ('empowering', 'Empowering & Strong'),
            ('practical', 'Practical & Grounded'),
            ('spiritual', 'Spiritual & Soulful'),
        ],
        default='gentle',
        help_text="Preferred support style"
    )
    life_roles = models.JSONField(
        default=list,
        blank=True,
        help_text="Life roles - mother, professional, etc."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class RitualUsage(models.Model):
    """Track which rituals users try and their effectiveness ratings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ritual = models.ForeignKey('journal.Ritual', on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)
    
    # Effectiveness tracking
    was_helpful = models.BooleanField(null=True, blank=True, help_text="Did this ritual help?")
    effectiveness_rating = models.IntegerField(
        choices=[
            (1, 'Not helpful at all'),
            (2, 'Somewhat helpful'),
            (3, 'Moderately helpful'),
            (4, 'Very helpful'),
            (5, 'Extremely helpful'),
        ],
        null=True,
        blank=True,
        help_text="How effective was this ritual?"
    )
    
    # Usage context
    mood_before = models.CharField(
        max_length=20,
        choices=[
            ('happy', 'Happy'),
            ('sad', 'Sad'),
            ('anxious', 'Anxious'),
            ('calm', 'Calm'),
            ('stressed', 'Stressed'),
            ('excited', 'Excited'),
        ],
        blank=True,
        null=True,
        help_text="How were you feeling before the ritual?"
    )
    
    mood_after = models.CharField(
        max_length=20,
        choices=[
            ('happy', 'Happy'),
            ('sad', 'Sad'),
            ('anxious', 'Anxious'),
            ('calm', 'Calm'),
            ('stressed', 'Stressed'),
            ('excited', 'Excited'),
        ],
        blank=True,
        null=True,
        help_text="How were you feeling after the ritual?"
    )
    
    notes = models.TextField(blank=True, help_text="Any additional thoughts about this ritual")
    
    class Meta:
        unique_together = ['user', 'ritual', 'used_at']
        ordering = ['-used_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.ritual.title} ({self.used_at.date()})"
