from django.urls import path
from .views import GentleOnboardingView, PersonalizedWisdomView

urlpatterns = [
    path('onboarding/', GentleOnboardingView.as_view(), name='gentle-onboarding'),
    path('wisdom/', PersonalizedWisdomView.as_view(), name='personalized-wisdom'),
] 