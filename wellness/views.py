from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import WisdomMessage, UserWisdomDelivery, UserProfile, RitualUsage, MindfulnessActivity
from .serializers import (
    WisdomMessageSerializer, 
    UserWisdomDeliverySerializer, 
    UserProfileSerializer, 
    RitualUsageSerializer,
    MindfulnessActivitySerializer
)
from django.utils import timezone
from rest_framework import status
from journal.models import Ritual
from journal.serializers import RitualSerializer
from django.db import models

# Create your views here.

class GentleOnboardingView(APIView):
    """Initial gentle questions for new users (save to UserProfile)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            profile, created = UserProfile.objects.update_or_create(
                user=request.user,
                defaults=serializer.validated_data
            )
            return Response({
                "message": "Onboarding data saved.",
                "profile": UserProfileSerializer(profile).data
            })
        return Response(serializer.errors, status=400)

class PersonalizedWisdomView(APIView):
    """Get personalized wisdom message based on user's current state (stub logic)"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Example: Use query params or user profile to filter wisdom messages
        mood_context = request.query_params.get('mood_context', 'any')
        support_style = request.query_params.get('support_style', 'any')
        energy_level = request.query_params.get('energy_level', 'any')

        wisdom = WisdomMessage.objects.filter(
            is_active=True
        ).filter(
            for_mood_context__in=[mood_context, 'any'],
            for_support_style__in=[support_style, 'any'],
            for_energy_level__in=[energy_level, 'any']
        ).order_by('?').first()

        if wisdom:
            serializer = WisdomMessageSerializer(wisdom)
            # Optionally, log delivery
            UserWisdomDelivery.objects.create(user=request.user, wisdom_message=wisdom)
            return Response(serializer.data)
        return Response({"detail": "No wisdom message found."}, status=status.HTTP_404_NOT_FOUND)

class PersonalizedRitualsView(APIView):
    """Get personalized ritual recommendations based on user's profile and effectiveness history"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get personalized ritual recommendations with effectiveness consideration"""
        try:
            # Get user's profile
            profile = UserProfile.objects.get(user=request.user)
            
            # Get user's ritual effectiveness history
            user_usage = RitualUsage.objects.filter(user=request.user)
            highly_rated_rituals = user_usage.filter(effectiveness_rating__gte=4).values_list('ritual_id', flat=True)
            low_rated_rituals = user_usage.filter(effectiveness_rating__lte=2).values_list('ritual_id', flat=True)
            
            # Build filter based on user's profile
            filters = {'is_active': True}
            
            # Match life phase (mood context)
            if profile.current_mood_context:
                filters['for_life_phase__in'] = [profile.current_mood_context, 'any']
            
            # Match emotional tone (support style)
            if profile.preferred_support_style:
                # Map support style to emotional tone
                style_to_tone = {
                    'gentle': 'gentle',
                    'empowering': 'empowering', 
                    'practical': 'grounding',
                    'spiritual': 'healing'
                }
                tone = style_to_tone.get(profile.preferred_support_style, 'gentle')
                filters['emotional_tone__in'] = [tone, 'gentle']  # fallback to gentle
            
            # Get matching rituals
            base_rituals = Ritual.objects.filter(**filters)
            
            # Prioritize highly rated rituals
            if highly_rated_rituals:
                # Include highly rated rituals that match current filters
                highly_rated_matches = base_rituals.filter(id__in=highly_rated_rituals)
                if highly_rated_matches.exists():
                    rituals = list(highly_rated_matches.order_by('?')[:3])
                    # Fill remaining slots with other matching rituals
                    remaining_rituals = base_rituals.exclude(id__in=highly_rated_rituals).exclude(id__in=low_rated_rituals).order_by('?')[:2]
                    rituals.extend(remaining_rituals)
                else:
                    rituals = list(base_rituals.exclude(id__in=low_rated_rituals).order_by('?')[:5])
            else:
                # No history yet, use standard matching
                rituals = list(base_rituals.exclude(id__in=low_rated_rituals).order_by('?')[:5])
            
            if rituals:
                serializer = RitualSerializer(rituals, many=True)
                
                # Add effectiveness context
                effectiveness_context = {
                    "total_rituals_tried": user_usage.count(),
                    "highly_rated_count": len(highly_rated_rituals),
                    "recommendation_basis": "effectiveness_history" if highly_rated_rituals else "profile_matching"
                }
                
                return Response({
                    "message": "Personalized rituals for you",
                    "user_context": {
                        "mood_context": profile.current_mood_context,
                        "support_style": profile.preferred_support_style
                    },
                    "effectiveness_context": effectiveness_context,
                    "rituals": serializer.data
                })
            else:
                # Fallback to any active rituals
                fallback_rituals = Ritual.objects.filter(is_active=True).exclude(id__in=low_rated_rituals).order_by('?')[:3]
                serializer = RitualSerializer(fallback_rituals, many=True)
                return Response({
                    "message": "Here are some gentle rituals for you",
                    "rituals": serializer.data
                })
                
        except UserProfile.DoesNotExist:
            # User hasn't completed onboarding, return general rituals
            general_rituals = Ritual.objects.filter(is_active=True, is_for_beginners=True).order_by('?')[:3]
            serializer = RitualSerializer(general_rituals, many=True)
            return Response({
                "message": "Welcome! Here are some beginner-friendly rituals",
                "rituals": serializer.data
            })

class UserProfileView(APIView):
    """View and update user profile"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's current profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        """Update user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class RitualTrackingView(APIView):
    """Track ritual usage and effectiveness"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Mark a ritual as used and optionally rate its effectiveness"""
        try:
            print(f"Received request data: {request.data}")  # Debug log
            
            # Get language from request headers or default to English
            language = request.META.get('HTTP_ACCEPT_LANGUAGE', 'en')[:2].lower()
            if language not in ['en', 'ka']:
                language = 'en'
                
            serializer = RitualUsageSerializer(data=request.data)
            if not serializer.is_valid():
                print(f"Serializer errors: {serializer.errors}")  # Debug log
                return Response({
                    "detail": "Invalid data provided.",
                    "errors": serializer.errors
                }, status=400)
            
            # Get ritual ID from the data
            ritual_id = request.data.get('ritual')
            if not ritual_id:
                return Response({"detail": "Ritual ID is required."}, status=400)
                
            # Convert ritual_id to integer if it's a string
            try:
                ritual_id = int(ritual_id) if isinstance(ritual_id, str) else ritual_id
            except (ValueError, TypeError):
                return Response({
                    "detail": "Invalid ritual ID format. Must be a number.",
                    "ritual_id": ritual_id
                }, status=400)
            
            # Ensure the ritual exists and is active
            try:
                ritual = Ritual.objects.get(id=ritual_id, is_active=True)
            except Ritual.DoesNotExist:
                return Response({
                    "detail": "Ritual not found or inactive.",
                    "ritual_id": ritual_id,
                    "available_rituals": list(Ritual.objects.filter(is_active=True).values('id', 'title', 'language'))
                }, status=404)
            
            # Create usage record with the ritual
            usage_data = serializer.validated_data.copy()
            usage_data['ritual'] = ritual
            
            try:
                usage = RitualUsage.objects.create(
                    user=request.user,
                    **usage_data
                )
                
                return Response({
                    "message": "Ritual usage tracked successfully.",
                    "usage": RitualUsageSerializer(usage).data
                })
                
            except Exception as e:
                print(f"Error creating RitualUsage: {str(e)}")  # Debug log
                return Response({
                    "detail": f"Error saving ritual usage: {str(e)}",
                    "error_type": type(e).__name__
                }, status=500)
                
        except Exception as e:
            print(f"Unexpected error in RitualTrackingView: {str(e)}")  # Debug log
            return Response({
                "detail": "An unexpected error occurred.",
                "error": str(e),
                "error_type": type(e).__name__
            }, status=500)

class RitualHistoryView(APIView):
    """Get user's ritual usage history"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's ritual usage history with effectiveness data"""
        # Get all ritual usages for the user
        usages = RitualUsage.objects.filter(user=request.user).select_related('ritual').order_by('-used_at')
        
        # Calculate stats
        total_rituals = usages.count()
        helpful_rituals = usages.filter(was_helpful=True).count()
        
        # Calculate average rating (excluding nulls)
        ratings = usages.exclude(effectiveness_rating__isnull=True).values_list('effectiveness_rating', flat=True)
        avg_rating = sum(ratings) / len(ratings) if ratings else None
        
        # Serialize the data
        serializer = RitualUsageSerializer(usages, many=True)
        
        return Response({
            'history': serializer.data,
            'stats': {
                'total_rituals_used': total_rituals,
                'helpful_rituals': helpful_rituals,
                'average_rating': round(avg_rating, 1) if avg_rating is not None else None,
            }
        })

class TestMindfulnessView(APIView):
    """Test endpoint to help diagnose issues"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Simple test endpoint to check if basic functionality works"""
        try:
            # Just return a simple response to test the endpoint
            return Response({
                "status": "success",
                "message": "Test endpoint is working",
                "user": request.user.username,
                "timestamp": timezone.now().isoformat()
            })
        except Exception as e:
            return Response(
                {"error": str(e), "type": type(e).__name__},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class SimpleMindfulnessActivityView(APIView):
    """Simplified version of MindfulnessActivityView for debugging"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Return a simplified list of activities"""
        try:
            # Get basic activity data without any complex serialization
            activities = MindfulnessActivity.objects.filter(is_active=True).values(
                'id', 'title', 'description', 'duration_minutes', 'category'
            )
            
            return Response({
                "status": "success",
                "count": len(activities),
                "activities": list(activities)
            })
            
        except Exception as e:
            import traceback
            return Response(
                {
                    "status": "error",
                    "error": str(e),
                    "type": type(e).__name__,
                    "traceback": traceback.format_exc()
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MindfulnessActivityView(APIView):
    """View for mindfulness activities"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get all active mindfulness activities"""
        try:
            # Check authentication
            if not request.user.is_authenticated:
                return Response(
                    {"detail": "Authentication credentials were not provided."}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
                
            # Get language from query params or default to English
            language = request.query_params.get('lang', 'en')
            
            # Debug logging
            print(f"\n=== Debug: Starting MindfulnessActivityView.get() ===")
            print(f"1. User: {request.user.username}")
            print(f"2. Language: {language}")
            
            # Get active activities with explicit select_related and prefetch_related
            print("3. Fetching activities from database...")
            try:
                activities = MindfulnessActivity.objects.filter(is_active=True)
                print(f"4. Queryset SQL: {str(activities.query)}")
                
                # Force evaluation of the queryset to catch any database errors
                count = activities.count()
                print(f"5. Found {count} activities")
                
                # Log model fields and related objects
                print("6. Model fields:", [f.name for f in MindfulnessActivity._meta.get_fields()])
                print("7. Model related objects:", [f.name for f in MindfulnessActivity._meta.related_objects])
                
            except Exception as db_error:
                print(f"!!! Database error: {str(db_error)}")
                print("!!! Exception type:", type(db_error).__name__)
                import traceback
                print("!!! Traceback:", traceback.format_exc())
                raise
            
            # Debug: Print the raw queryset SQL
            print("3. Raw SQL query:", str(activities.query))
            
            # Debug: Check if the queryset has any prefetch_related calls
            if hasattr(activities, '_prefetch_related_lookups'):
                print("4. Prefetch related lookups:", activities._prefetch_related_lookups)
            else:
                print("4. No prefetch_related lookups found on the queryset")
            
            # Debug: Print the model's _meta to check fields and related_objects
            print("5. Model fields:", [f.name for f in MindfulnessActivity._meta.get_fields()])
            print("6. Model related objects:", [f.name for f in MindfulnessActivity._meta.related_objects])
            
            # Initialize serializer with request context for language handling and URL resolution
            print("8. Initializing serializer...")
            try:
                # Create a list from the queryset to prevent any lazy evaluation issues
                activities_list = list(activities)
                print(f"9. Converted queryset to list with {len(activities_list)} items")
                
                # Log the first activity for debugging
                if activities_list:
                    first_activity = activities_list[0]
                    print(f"10. First activity ID: {first_activity.id}, Title: {first_activity.title}")
                    print(f"11. First activity audio_file: {getattr(first_activity, 'audio_file', 'None')}")
                
                # Initialize the serializer
                serializer_context = {
                    'request': request,
                    'language': language
                }
                print("12. Serializer context:", serializer_context)
                
                serializer = MindfulnessActivitySerializer(
                    activities_list,
                    many=True,
                    context=serializer_context
                )
                print("13. Serializer initialized successfully")
                
                # Get serialized data with error handling
                try:
                    serialized_data = serializer.data
                    print(f"14. Successfully serialized {len(serialized_data) if serialized_data else 0} activities")
                    if serialized_data and len(serialized_data) > 0:
                        print("15. First serialized activity keys:", list(serialized_data[0].keys()))
                except Exception as ser_error:
                    print(f"!!! Error accessing serializer.data: {str(ser_error)}")
                    print("!!! Exception type:", type(ser_error).__name__)
                    import traceback
                    print("!!! Traceback:", traceback.format_exc())
                    raise
                    
            except Exception as e:
                print(f"!!! Error in serializer initialization: {str(e)}")
                print("!!! Exception type:", type(e).__name__)
                import traceback
                print("!!! Full traceback:")
                traceback.print_exc()
                
                # Return a more detailed error response
                return Response(
                    {
                        "error": "Error serializing mindfulness activities",
                        "details": str(e),
                        "type": type(e).__name__,
                        "traceback": traceback.format_exc() if settings.DEBUG else "Traceback only available in DEBUG mode"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Get serialized data
            serialized_data = serializer.data
            print(f"Serialized {len(serialized_data)} activities")
            
            # Debug: Print first activity's audio URL if available
            if serialized_data and 'audio_file' in serialized_data[0]:
                print(f"First activity audio URL: {serialized_data[0].get('audio_file')}")
            
            return Response(serializer.data)
            
        except Exception as e:
            # Log the full error
            import traceback
            error_trace = traceback.format_exc()
            print(f"Error in MindfulnessActivityView: {str(e)}\n{error_trace}")
            
            # Return a detailed error response
            return Response(
                {
                    "error": "An error occurred while fetching mindfulness activities.",
                    "details": str(e),
                    "trace": error_trace if settings.DEBUG else "Traceback only available in DEBUG mode"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class TrackMindfulnessActivityView(APIView):
    """Track when a user starts a mindfulness activity"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, activity_id=None):
        """Record that a user has started a mindfulness activity"""
        
        if not activity_id:
            return Response(
                {"error": "Activity ID is required in URL"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            activity = MindfulnessActivity.objects.get(id=activity_id, is_active=True)
        except MindfulnessActivity.DoesNotExist:
            return Response(
                {"error": "Invalid activity ID"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        # Record the activity usage
        # You might want to create a separate model for tracking mindfulness activity usage
        # For now, we'll just return a success response
        
        return Response({
            "message": "Mindfulness activity tracked successfully",
            "activity": MindfulnessActivitySerializer(activity).data
        })
