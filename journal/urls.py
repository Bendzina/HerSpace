from django.urls import path
from .views import JournalEntryListCreateView

urlpatterns = [
    path('journal-entries/', JournalEntryListCreateView.as_view(), name='journal-entry-list-create'),
]