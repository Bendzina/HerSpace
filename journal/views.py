from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import JournalEntry, MoodCheckIn, DailyTask
from .serializers import JournalEntrySerializer, MoodCheckInSerializer, DailyTaskSerializer

class JournalEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MoodCheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MoodCheckIn.objects.filter(user=self.request.user)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)