from django.urls import path
from .views import (
    ChildcareRoutineListCreateView, ChildcareRoutineDetailView,
    MotherhoodResourceListView, MotherhoodResourceDetailView,
    MotherhoodJournalListCreateView, MotherhoodJournalDetailView,
    SupportGroupListView, SupportGroupDetailView
)

urlpatterns = [
    # Childcare Routines
    path('routines/', ChildcareRoutineListCreateView.as_view(), name='childcare-routine-list-create'),
    path('routines/<int:pk>/', ChildcareRoutineDetailView.as_view(), name='childcare-routine-detail'),
    
    # Motherhood Resources
    path('resources/', MotherhoodResourceListView.as_view(), name='motherhood-resource-list'),
    path('resources/<int:pk>/', MotherhoodResourceDetailView.as_view(), name='motherhood-resource-detail'),
    
    # Motherhood Journal
    path('journal/', MotherhoodJournalListCreateView.as_view(), name='motherhood-journal-list-create'),
    path('journal/<int:pk>/', MotherhoodJournalDetailView.as_view(), name='motherhood-journal-detail'),
    
    # Support Groups
    path('support-groups/', SupportGroupListView.as_view(), name='support-group-list'),
    path('support-groups/<int:pk>/', SupportGroupDetailView.as_view(), name='support-group-detail'),
] 