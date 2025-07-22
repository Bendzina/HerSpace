# Register your models here.
from django.contrib import admin
from .models import JournalEntry, MoodCheckIn, DailyTask, Ritual

admin.site.register(JournalEntry)
admin.site.register(MoodCheckIn)
admin.site.register(DailyTask)
admin.site.register(Ritual)