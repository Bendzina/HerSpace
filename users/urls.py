from django.urls import path
from .views import (
    UserRegistrationView, 
    user_profile,
    VerifyEmailView,
    ResendVerificationEmail,
    CheckEmailVerificationView,
    UserStatsView,
)

urlpatterns = [
    path('auth/register/', UserRegistrationView.as_view(), name='user-register'),
    path('me/', user_profile, name='user_profile'),
    # Email verification URLs
    path('auth/verify-email/<uuid:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('auth/resend-verification/', ResendVerificationEmail.as_view(), name='resend-verification'),
    path('auth/check-email/', CheckEmailVerificationView.as_view(), name='check-email-verification'),
    path('stats/', UserStatsView.as_view(), name='user-stats'),
]