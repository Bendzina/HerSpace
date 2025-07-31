from django.urls import path
from .views import (
    NotificationListView, NotificationDetailView, NotificationCreateView,
    NotificationMarkReadView, NotificationPreferenceView,
    NotificationTemplateListView, NotificationStatsView
)

urlpatterns = [
    # Notifications
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
    path('create/', NotificationCreateView.as_view(), name='notification-create'),
    path('mark-read/', NotificationMarkReadView.as_view(), name='notification-mark-read'),
    
    # Preferences
    path('preferences/', NotificationPreferenceView.as_view(), name='notification-preferences'),
    
    # Templates
    path('templates/', NotificationTemplateListView.as_view(), name='notification-templates'),
    
    # Stats
    path('stats/', NotificationStatsView.as_view(), name='notification-stats'),
] 