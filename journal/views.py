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

        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        answer = response.choices[0].message.content
        return Response({"response": answer})