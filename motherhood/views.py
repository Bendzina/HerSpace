from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import ChildcareRoutine, MotherhoodResource, MotherhoodJournal, SupportGroup
from .serializers import (
    ChildcareRoutineSerializer, MotherhoodResourceSerializer, 
    MotherhoodJournalSerializer, SupportGroupSerializer
)

# Childcare Routine Views
class ChildcareRoutineListCreateView(generics.ListCreateAPIView):
    serializer_class = ChildcareRoutineSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['routine_type', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'time_of_day']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return ChildcareRoutine.objects.none()
        return ChildcareRoutine.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChildcareRoutineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChildcareRoutineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return ChildcareRoutine.objects.none()
        return ChildcareRoutine.objects.filter(user=user)

# Motherhood Resource Views
class MotherhoodResourceListView(generics.ListAPIView):
    serializer_class = MotherhoodResourceSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['resource_type', 'category', 'is_featured', 'is_active']
    search_fields = ['title', 'description', 'author']
    ordering_fields = ['created_at', 'title']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def get_queryset(self):
        return MotherhoodResource.objects.filter(is_active=True)

class MotherhoodResourceDetailView(generics.RetrieveAPIView):
    serializer_class = MotherhoodResourceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MotherhoodResource.objects.filter(is_active=True)

# Motherhood Journal Views
class MotherhoodJournalListCreateView(generics.ListCreateAPIView):
    serializer_class = MotherhoodJournalSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['mood', 'is_private', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return MotherhoodJournal.objects.none()
        return MotherhoodJournal.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MotherhoodJournalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MotherhoodJournalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return MotherhoodJournal.objects.none()
        return MotherhoodJournal.objects.filter(user=user)

# Support Group Views
class SupportGroupListView(generics.ListAPIView):
    serializer_class = SupportGroupSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['group_type', 'is_private', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def get_queryset(self):
        return SupportGroup.objects.filter(is_active=True)

class SupportGroupDetailView(generics.RetrieveAPIView):
    serializer_class = SupportGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SupportGroup.objects.filter(is_active=True)
