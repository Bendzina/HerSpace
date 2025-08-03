from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WisdomMessage, UserWisdomDelivery, UserProfile, RitualUsage
from .serializers import WisdomMessageSerializer, UserWisdomDeliverySerializer, UserProfileSerializer, RitualUsageSerializer
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
        serializer = RitualUsageSerializer(data=request.data)
        if serializer.is_valid():
            # Get ritual ID from the data
            ritual_id = request.data.get('ritual')
            if not ritual_id:
                return Response({"detail": "Ritual ID is required."}, status=400)
            
            # Ensure the ritual exists and is active
            try:
                ritual = Ritual.objects.get(id=ritual_id, is_active=True)
            except Ritual.DoesNotExist:
                return Response({"detail": "Ritual not found or inactive."}, status=404)
            
            # Create usage record with the ritual
            usage_data = serializer.validated_data.copy()
            usage_data['ritual'] = ritual
            
            usage = RitualUsage.objects.create(
                user=request.user,
                **usage_data
            )
            
            return Response({
                "message": "Ritual usage tracked successfully.",
                "usage": RitualUsageSerializer(usage).data
            })
        return Response(serializer.errors, status=400)

class RitualHistoryView(APIView):
    """Get user's ritual usage history"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's ritual usage history with effectiveness data"""
        usages = RitualUsage.objects.filter(user=request.user).select_related('ritual')
        serializer = RitualUsageSerializer(usages, many=True)
        
        # Calculate some basic stats
        total_used = usages.count()
        helpful_count = usages.filter(was_helpful=True).count()
        avg_rating = usages.aggregate(avg_rating=models.Avg('effectiveness_rating'))['avg_rating']
        
        return Response({
            "history": serializer.data,
            "stats": {
                "total_rituals_used": total_used,
                "helpful_rituals": helpful_count,
                "average_rating": round(avg_rating, 1) if avg_rating else None
            }
        })
