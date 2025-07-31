from django.urls import path
from .views import (
    MoodAnalyticsView, TaskAnalyticsView, JournalAnalyticsView, UserInsightsView
)

urlpatterns = [
    path('mood/', MoodAnalyticsView.as_view(), name='mood-analytics'),
    path('tasks/', TaskAnalyticsView.as_view(), name='task-analytics'),
    path('journal/', JournalAnalyticsView.as_view(), name='journal-analytics'),
    path('insights/', UserInsightsView.as_view(), name='user-insights'),
] 