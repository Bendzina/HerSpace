from rest_framework import generics
from .models import JournalEntry
from .serializers import JournalEntrySerializer

class JournalEntryListCreateView(generics.ListCreateAPIView):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
