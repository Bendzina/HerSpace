from django.shortcuts import render
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notification, NotificationPreference, NotificationTemplate
from .serializers import (
    NotificationSerializer, NotificationPreferenceSerializer,
    NotificationTemplateSerializer, NotificationMarkReadSerializer,
    NotificationCreateSerializer
)
from django.utils import timezone

# Create your views here.

class NotificationListView(generics.ListAPIView):
    """List user's notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['notification_type', 'is_read', 'priority', 'created_at']
    ordering_fields = ['created_at', 'priority']
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationDetailView(generics.RetrieveAPIView):
    """Get a specific notification"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class NotificationCreateView(generics.CreateAPIView):
    """Create a custom notification"""
    serializer_class = NotificationCreateSerializer
    permission_classes = [IsAuthenticated]

class NotificationMarkReadView(generics.UpdateAPIView):
    """Mark notifications as read"""
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, *args, **kwargs):
        serializer = NotificationMarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notification_ids = serializer.validated_data['notification_ids']
        notifications = Notification.objects.filter(
            user=request.user,
            id__in=notification_ids
        )
        
        # Mark as read
        notifications.update(is_read=True)
        
        return Response({
            "message": f"Marked {notifications.count()} notifications as read"
        })

class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    """Get and update user's notification preferences"""
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        # Get or create preferences for the user
        preferences, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences

class NotificationTemplateListView(generics.ListAPIView):
    """List notification templates (admin only)"""
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]
    queryset = NotificationTemplate.objects.filter(is_active=True)

class NotificationStatsView(generics.RetrieveAPIView):
    """Get notification statistics for user"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        
        stats = {
            'total_notifications': notifications.count(),
            'unread_count': notifications.filter(is_read=False).count(),
            'read_count': notifications.filter(is_read=True).count(),
            'high_priority_count': notifications.filter(priority='high', is_read=False).count(),
            'today_notifications': notifications.filter(created_at__date=timezone.now().date()).count(),
        }
        
        return Response(stats)
