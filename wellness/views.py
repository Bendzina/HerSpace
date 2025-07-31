from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WisdomMessage, UserWisdomDelivery
from .serializers import WisdomMessageSerializer, UserWisdomDeliverySerializer
from django.utils import timezone
from rest_framework import status

# Create your views here.

class GentleOnboardingView(APIView):
    """Initial gentle questions for new users (stub)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Here you would process onboarding data
        # For now, just echo back what was sent
        return Response({"message": "Onboarding data received.", "data": request.data})

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
