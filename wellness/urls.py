from django.urls import path
from .views import (
    GentleOnboardingView, PersonalizedWisdomView, UserProfileView, 
    PersonalizedRitualsView, RitualTrackingView, RitualHistoryView
)

urlpatterns = [
    path('onboarding/', GentleOnboardingView.as_view(), name='gentle-onboarding'),
    path('wisdom/', PersonalizedWisdomView.as_view(), name='personalized-wisdom'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('rituals/', PersonalizedRitualsView.as_view(), name='personalized-rituals'),
    path('rituals/track/', RitualTrackingView.as_view(), name='ritual-tracking'),
    path('rituals/history/', RitualHistoryView.as_view(), name='ritual-history'),
] 