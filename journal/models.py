
from django.db import models
from django.conf import settings
from django.utils import timezone

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, blank=True, default='')
    content = models.TextField()

class MoodCheckIn(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('anxious', 'Anxious'),
        ('calm', 'Calm'),
        
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True, null=True)
    
    # New Gentle Fields
    energy_level = models.IntegerField(
        choices=[
            (1, 'Very Low'),
            (2, 'Low'),
            (3, 'Moderate'),
            (4, 'High'),
            (5, 'Very High'),
        ],
        help_text="Energy level",
        null=True,
        blank=True
    )
    
    needs_today = models.TextField(
        max_length=500,
        blank=True,
        help_text="What do you need today?"
    )
    
    gratitude_moment = models.TextField(
        max_length=300,
        blank=True,
        help_text="Gratitude moment"
    )
    
    emotional_support_needed = models.CharField(
        max_length=30,
        choices=[
            ('listening', 'Just Need to Be Heard'),
            ('guidance', 'Need Gentle Guidance'),
            ('encouragement', 'Need Encouragement'),
            ('grounding', 'Need Grounding'),
            ('celebration', 'Want to Celebrate'),
        ],
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'date']

class DailyTask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    body_task = models.CharField(max_length=255)
    work_task = models.CharField(max_length=255)
    soul_task = models.CharField(max_length=255)
    completed = models.BooleanField(default=False) # type: ignore
    
class Ritual(models.Model):
    RITUAL_TYPE_CHOICES = [
        ('meditation', 'Meditation'),
        ('affirmation', 'Affirmation'),
        ('prompt', 'Journaling Prompt'),
        ('tarot', 'Tarot Reflection'),
        # add more as needed
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ritual_type = models.CharField(max_length=30, choices=RITUAL_TYPE_CHOICES)
    content = models.TextField()
    
    # New Gentle Fields
    for_life_phase = models.CharField(
        max_length=50,
        choices=[
            ('any', 'Any Phase'),
            ('transition', 'Life Transition'),
            ('motherhood', 'Motherhood'),
            ('career_stress', 'Career Stress'),
            ('healing', 'Healing Journey'),
            ('self_discovery', 'Self Discovery'),
        ],
        default='any',
        help_text="For which life phase"
    )
    
    emotional_tone = models.CharField(
        max_length=30,
        choices=[
            ('gentle', 'Gentle & Soothing'),
            ('empowering', 'Empowering & Strong'),
            ('grounding', 'Grounding & Centering'),
            ('uplifting', 'Uplifting & Joyful'),
            ('healing', 'Healing & Restorative'),
        ],
        default='gentle'
    )
    
    duration_minutes = models.IntegerField(
        default=5,
        help_text="Duration in minutes"
    )
    
    is_for_beginners = models.BooleanField(default=True)
    tags = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.ritual_type})"