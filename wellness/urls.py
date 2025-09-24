from django.urls import path
from .views import (
    GentleOnboardingView, PersonalizedWisdomView, UserProfileView, 
    PersonalizedRitualsView, RitualTrackingView, RitualHistoryView,
    MindfulnessActivityView, TrackMindfulnessActivityView, TestMindfulnessView,
    SimpleMindfulnessActivityView
)

urlpatterns = [
    path('onboarding/', GentleOnboardingView.as_view(), name='gentle-onboarding'),
    path('wisdom/', PersonalizedWisdomView.as_view(), name='personalized-wisdom'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('rituals/', PersonalizedRitualsView.as_view(), name='personalized-rituals'),
    path('rituals/track/', RitualTrackingView.as_view(), name='ritual-tracking'),
    path('rituals/history/', RitualHistoryView.as_view(), name='ritual-history'),
    
    # Mindfulness endpoints
    path('mindfulness/test/', TestMindfulnessView.as_view(), name='mindfulness-test'),
    path('mindfulness/simple-activities/', SimpleMindfulnessActivityView.as_view(), name='simple-mindfulness-activities'),
    path('mindfulness/activities/', MindfulnessActivityView.as_view(), name='mindfulness-activities'),
    path('mindfulness/activities/track/', TrackMindfulnessActivityView.as_view(), name='track-mindfulness-activity'),
] 