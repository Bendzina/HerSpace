from django.urls import path
from .views import UserRegistrationView, user_profile

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('me/', user_profile, name='user_profile'), 
]