from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import JournalEntry, MoodCheckIn, DailyTask, Ritual
from .serializers import JournalEntrySerializer, MoodCheckInSerializer, DailyTaskSerializer, RitualSerializer
import openai
from django.conf import settings
from rest_framework.views import APIView
from .serializers import GPTPromptSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class JournalEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['created_at']  # filter by date
    search_fields = ['content']        # search in content
    ordering_fields = ['created_at']   # order by date
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(user=user)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MoodCheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['created_at']
    search_fields = ['content']
    ordering_fields = ['created_at']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]    
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return MoodCheckIn.objects.none()
        return MoodCheckIn.objects.filter(user=user)  # type: ignore
    
    def perform_create(self, serializer):
        today = timezone.now().date()
        user = self.request.user
        if MoodCheckIn.objects.filter(user=user, date=today).exists():
            raise ValidationError("You have already submitted a mood check-in for today.")
        serializer.save(user=user, date=today)
        
class DailyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['created_at']
    search_fields = ['content']
    ordering_fields = ['created_at']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return DailyTask.objects.none()
        return DailyTask.objects.filter(user=user)  # type: ignore
    
    def perform_create(self, serializer):
        today = timezone.now().date()
        user = self.request.user
        if DailyTask.objects.filter(user=user, date=today).exists():
            raise ValidationError("You have already created a daily task for today.")
        serializer.save(user=user, date=today)

# Note: Mood analytics are provided by analytics.app at /api/analytics/mood/.
# We intentionally do not duplicate analytics logic here in the journal app.

# Detail views for each model
class JournalEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)  # type: ignore

class MoodCheckInDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodCheckIn.objects.filter(user=self.request.user)  # type: ignore

class DailyTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)  # type: ignore

class RitualListCreateView(generics.ListCreateAPIView):
    serializer_class = RitualSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ritual.objects.filter(is_active=True)
    
class RitualDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RitualSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ritual.objects.filter(is_active=True)
    
# GPT Response View

class GPTAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GPTPromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prompt = serializer.validated_data['prompt']

        # client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        # response = client.chat.completions.create(
        #     model="gpt-4o",
        #     messages=[{"role": "user", "content": prompt}],
        #     max_tokens=200
        # )
        # answer = response.choices[0].message.content
        return Response({"message": "This is a temporary answer until the OpenAI API becomes active."})
