from django.urls import path
from .views import JournalEntryListCreateView, MoodCheckInListCreateView, DailyTaskListCreateView

urlpatterns = [
    path('journal-entries/', JournalEntryListCreateView.as_view(), name='journal-entry-list-create'),
    path('mood-checkins/', MoodCheckInListCreateView.as_view(), name='mood-checkin-list-create'),
    path('daily-tasks/', DailyTaskListCreateView.as_view(), name='daily-task-list-create'),
]