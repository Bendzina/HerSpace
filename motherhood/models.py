from django.db import models
from django.conf import settings

class ChildcareRoutine(models.Model):
    """Daily childcare routines and schedules"""
    ROUTINE_TYPE_CHOICES = [
        ('feeding', 'Feeding'),
        ('sleep', 'Sleep'),
        ('play', 'Play'),
        ('hygiene', 'Hygiene'),
        ('medical', 'Medical'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    routine_type = models.CharField(max_length=20, choices=ROUTINE_TYPE_CHOICES)
    description = models.TextField()
    time_of_day = models.TimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.routine_type})"

class MotherhoodResource(models.Model):
    """Curated resources for mothers"""
    RESOURCE_TYPE_CHOICES = [
        ('article', 'Article'),
        ('video', 'Video'),
        ('podcast', 'Podcast'),
        ('book', 'Book'),
        ('app', 'App'),
        ('community', 'Community'),
        ('professional', 'Professional Help'),
    ]
    
    CATEGORY_CHOICES = [
        ('pregnancy', 'Pregnancy'),
        ('newborn', 'Newborn Care'),
        ('toddler', 'Toddler Development'),
        ('preschool', 'Preschool Age'),
        ('school_age', 'School Age'),
        ('teen', 'Teen Parenting'),
        ('self_care', 'Self-Care'),
        ('relationships', 'Relationships'),
        ('mental_health', 'Mental Health'),
        ('work_life', 'Work-Life Balance'),
    ]
    
    title = models.CharField(max_length=255)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    url = models.URLField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

class MotherhoodJournal(models.Model):
    """Specialized journaling for motherhood experiences"""
    MOOD_CHOICES = [
        ('overwhelmed', 'Overwhelmed'),
        ('joyful', 'Joyful'),
        ('exhausted', 'Exhausted'),
        ('grateful', 'Grateful'),
        ('frustrated', 'Frustrated'),
        ('proud', 'Proud'),
        ('anxious', 'Anxious'),
        ('peaceful', 'Peaceful'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES, blank=True)
    is_private = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"

class RitualCompletion(models.Model):
    """Tracks completion of motherhood rituals and routines"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    routine = models.ForeignKey('ChildcareRoutine', on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-completed_at']
        verbose_name = 'Ritual Completion'
        verbose_name_plural = 'Ritual Completions'

    def __str__(self):
        return f"{self.user.email} - {self.routine.title if self.routine else 'Custom Ritual'} - {self.completed_at.strftime('%Y-%m-%d %H:%M')}"


class SupportGroup(models.Model):
    """Virtual support groups for mothers"""
    GROUP_TYPE_CHOICES = [
        ('pregnancy', 'Pregnancy Support'),
        ('newborn', 'Newborn Support'),
        ('single_mom', 'Single Mom Support'),
        ('working_mom', 'Working Mom Support'),
        ('mental_health', 'Mental Health Support'),
        ('general', 'General Motherhood'),
    ]
    
    name = models.CharField(max_length=255)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPE_CHOICES)
    description = models.TextField()
    is_private = models.BooleanField(default=True)
    max_members = models.IntegerField(default=50)
    current_members = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group_type})"
