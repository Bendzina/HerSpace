from django.urls import path
from .views import (
    JournalEntryListCreateView, MoodCheckInListCreateView, DailyTaskListCreateView,
    JournalEntryDetailView, MoodCheckInDetailView, DailyTaskDetailView,
    RitualListCreateView, RitualDetailView, GPTAssistantView,
    TarotCardListView, TarotPromptListCreateView, TarotPromptDetailView,
    AIConversationListCreateView, AIConversationDetailView
)

urlpatterns = [
    path('journal-entries/', JournalEntryListCreateView.as_view(), name='journal-entry-list-create'),
    path('journal-entries/<int:pk>/', JournalEntryDetailView.as_view(), name='journal-entry-detail'),
    path('mood-checkins/', MoodCheckInListCreateView.as_view(), name='mood-checkin-list-create'),
    path('mood-checkins/<int:pk>/', MoodCheckInDetailView.as_view(), name='mood-checkin-detail'),
    path('daily-tasks/', DailyTaskListCreateView.as_view(), name='daily-task-list-create'),
    path('daily-tasks/<int:pk>/', DailyTaskDetailView.as_view(), name='daily-task-detail'),
    path('rituals/', RitualListCreateView.as_view(), name='ritual-list-create'),
    path('rituals/<int:pk>/', RitualDetailView.as_view(), name='ritual-detail'),

    # Dagi AI endpoints
    path('dagi-ai/', GPTAssistantView.as_view(), name='dagi-ai'),

    # Tarot endpoints
    path('tarot/cards/', TarotCardListView.as_view(), name='tarot-card-list'),
    path('tarot/readings/', TarotPromptListCreateView.as_view(), name='tarot-reading-list-create'),
    path('tarot/readings/<int:pk>/', TarotPromptDetailView.as_view(), name='tarot-reading-detail'),

    # AI Conversation endpoints
    path('ai/conversations/', AIConversationListCreateView.as_view(), name='ai-conversation-list-create'),
    path('ai/conversations/<int:pk>/', AIConversationDetailView.as_view(), name='ai-conversation-detail'),
]
