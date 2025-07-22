from django.urls import path
from .views import JournalEntryListCreateView, MoodCheckInListCreateView, DailyTaskListCreateView, JournalEntryDetailView, MoodCheckInDetailView, DailyTaskDetailView, RitualListCreateView, RitualDetailView, GPTAssistantView

urlpatterns = [
    path('journal-entries/', JournalEntryListCreateView.as_view(), name='journal-entry-list-create'),
    path('journal-entries/<int:pk>/', JournalEntryDetailView.as_view(), name='journal-entry-detail'),
    path('mood-checkins/', MoodCheckInListCreateView.as_view(), name='mood-checkin-list-create'),
    path('mood-checkins/<int:pk>/', MoodCheckInDetailView.as_view(), name='mood-checkin-detail'),
    path('daily-tasks/', DailyTaskListCreateView.as_view(), name='daily-task-list-create'),
    path('daily-tasks/<int:pk>/', DailyTaskDetailView.as_view(), name='daily-task-detail'),
    path('rituals/', RitualListCreateView.as_view(), name='ritual-list-create'),
    path('rituals/<int:pk>/', RitualDetailView.as_view(), name='ritual-detail'),
    # GPT Assistant View
    path('dagi-ai/', GPTAssistantView.as_view(), name='dagi-ai'),
]
