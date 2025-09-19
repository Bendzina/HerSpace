from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from django.contrib.auth import get_user_model
import logging
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes
from .models import EmailVerification
from .email_service import send_verification_email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from journal.models import JournalEntry
from motherhood.models import RitualCompletion
from django.utils import timezone
from datetime import timedelta
logger = logging.getLogger(__name__)
User = get_user_model()
import uuid
from django.utils import timezone
from rest_framework.permissions import AllowAny

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create verification record
            verification = EmailVerification.objects.create(user=user)
            # Send verification email
            send_verification_email(user, verification.token, request)
            return Response(
                {'message': 'Registration successful. Please check your email to verify your account.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# ✅ განახლებული user_profile ფუნქცია - GET და PATCH support
@api_view(['GET', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Current user-ის ინფორმაცია და განახლება"""
    try:
        if request.method == 'GET':
            # GET request - user info დაბრუნება
            user_data = {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'displayName': request.user.first_name or request.user.username,
            }
            return Response(user_data, status=status.HTTP_200_OK)
        
        elif request.method == 'PATCH':
            # PATCH request - user profile განახლება
            user = request.user
            
            if 'displayName' in request.data:
                user.first_name = request.data['displayName']
                user.save()
                logger.info(f"User {user.username} updated displayName to: {request.data['displayName']}")
            
            # განახლებული user data დაბრუნება
            updated_user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'displayName': user.first_name or user.username,
            }
            return Response(updated_user_data, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"User profile error: {str(e)}")
        return Response(
            {'error': 'Failed to process user profile request'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ✅ შენი class-based view კარგია, მაგრამ URL-ში არ იყენებ - შეძლებ წაშალო ან დატოვო backup-ისთვის
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile info"""
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'displayName': user.first_name or user.username,
        })
    
    def patch(self, request):
        """Update user profile"""
        user = request.user
        
        if 'displayName' in request.data:
            user.first_name = request.data['displayName']
            user.save()
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'displayName': user.first_name or user.username,
        })
        
# users/views.py
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        try:
            verification = EmailVerification.objects.select_related('user').get(token=token)
            
            if verification.is_verified:
                return Response(
                    {'message': 'Email already verified.'},
                    status=status.HTTP_200_OK
                )
                
            if verification.is_expired():
                # Option to resend verification
                return Response(
                    {'error': 'Verification link has expired. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Mark as verified
            verification.is_verified = True
            verification.save()
            
            # Activate the user
            user = verification.user
            user.is_active = True
            user.save(update_fields=['is_active'])
            
            return Response(
                {'message': 'Email successfully verified. You can now log in.'},
                status=status.HTTP_200_OK
            )
            
        except EmailVerification.DoesNotExist:
            return Response(
                {'error': 'Invalid verification token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
# Add this to users/views.py
class ResendVerificationEmail(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user = get_user_model().objects.get(email=email)
            verification, created = EmailVerification.objects.get_or_create(
                user=user,
                defaults={'token': uuid.uuid4()}
            )
            
            if not created and verification.is_verified:
                return Response(
                    {'message': 'Email is already verified.'},
                    status=status.HTTP_200_OK
                )
                
            # Update token if expired
            if verification.is_expired():
                verification.token = uuid.uuid4()
                verification.created_at = timezone.now()
                verification.save()
                
            send_verification_email(user, verification.token, request)
            
            return Response(
                {'message': 'Verification email sent.'},
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            # Don't reveal if user exists for security
            return Response(
                {'message': 'If an account exists with this email, a verification link has been sent.'},
                status=status.HTTP_200_OK
            )


class CheckEmailVerificationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response(
                {'error': 'Email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user = get_user_model().objects.get(email=email)
            is_verified = EmailVerification.objects.filter(
                user=user,
                is_verified=True
            ).exists()
            
            return Response({
                'exists': True,
                'is_verified': is_verified,
                'email': user.email,
                'user_id': user.id
            })
            
        except get_user_model().DoesNotExist:
            return Response({
                'exists': False,
                'is_verified': False,
                'email': email,
                'message': 'No account found with this email.'
            }, status=status.HTTP_200_OK)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Calculate day streak (example implementation)
        today = timezone.now().date()
        streak = 0
        current_date = today
        
        # Check for journal entries in the last 7 days as an example
        while True:
            has_entry = JournalEntry.objects.filter(
                user=user,
                created_at__date=current_date
            ).exists()
            
            if has_entry:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
        
        # Count total journal entries
        journal_entries = JournalEntry.objects.filter(user=user).count()
        
        # Count completed rituals (example)
        rituals_completed = RitualCompletion.objects.filter(
            user=user,
            completed=True
        ).count()
        
        return Response({
            'day_streak': streak,
            'journal_entries': journal_entries,
            'rituals_completed': rituals_completed,
        })