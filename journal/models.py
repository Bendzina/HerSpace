
from django.db import models
from django.conf import settings

class JournalEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
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
    ritual_type = models.CharField(max_length=30, choices=RITUAL_TYPE_CHOICES)
    content = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.ritual_type})"