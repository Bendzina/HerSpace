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

class MindfulnessActivity(models.Model):
    """Mindfulness activities for users to practice"""
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed description of the activity")
    short_description = models.CharField(max_length=255, blank=True, help_text="Brief description for cards")
    icon = models.CharField(max_length=50, default='leaf', help_text="Icon name from the icon set")
    duration_minutes = models.PositiveIntegerField(default=5, help_text="Estimated duration in minutes")
    audio_file = models.FileField(upload_to='mindfulness/audio/', blank=True, null=True)
    image = models.ImageField(upload_to='mindfulness/images/', blank=True, null=True)
    
    # Categorization
    ACTIVITY_CATEGORIES = [
        ('breathing', 'Breathing Exercises'),
        ('meditation', 'Meditation'),
        ('body_scan', 'Body Scan'),
        ('gratitude', 'Gratitude Practice'),
        ('visualization', 'Visualization'),
        ('movement', 'Gentle Movement'),
    ]
    
    category = models.CharField(
        max_length=50,
        choices=ACTIVITY_CATEGORIES,
        default='meditation',
        help_text="Type of mindfulness activity"
    )
    
    # Difficulty level
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_LEVELS,
        default='beginner',
        help_text="Difficulty level of the activity"
    )
    
    # Localization
    title_ka = models.CharField(max_length=200, blank=True, help_text="Title in Georgian")
    description_ka = models.TextField(blank=True, help_text="Description in Georgian")
    short_description_ka = models.CharField(max_length=255, blank=True, help_text="Short description in Georgian")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_title(self, language='en'):
        """Get localized title"""
        if language == 'ka' and self.title_ka:
            return self.title_ka
        return self.title
    
    def get_description(self, language='en'):
        """Get localized description"""
        if language == 'ka' and self.description_ka:
            return self.description_ka
        return self.description
    
    def get_short_description(self, language='en'):
        """Get localized short description"""
        if language == 'ka' and self.short_description_ka:
            return self.short_description_ka
        return self.short_description or self.description[:150] + ('...' if len(self.description) > 150 else '')

class MindfulnessSession(models.Model):
    """Track user's mindfulness practice sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mindfulness_sessions')
    activity = models.ForeignKey(MindfulnessActivity, on_delete=models.PROTECT, related_name='sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.PositiveIntegerField(help_text="Actual duration in minutes")
    
    # Optional feedback
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
        help_text="How were you feeling before the session?"
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
        help_text="How are you feeling after the session?"
    )
    
    notes = models.TextField(blank=True, help_text="Any reflections or notes about this session")
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.activity.title} at {self.started_at}"
