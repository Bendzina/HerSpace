from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import JournalEntry, MoodCheckIn, DailyTask, Ritual, TarotCard, TarotPrompt, TarotDeck, AIConversation
from .serializers import JournalEntrySerializer, MoodCheckInSerializer, DailyTaskSerializer, RitualSerializer, TarotCardSerializer, TarotPromptSerializer, TarotDeckSerializer, AIConversationSerializer
import openai
from django.conf import settings
from rest_framework.views import APIView
from .serializers import GPTPromptSerializer
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import random
import json

class JournalEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['created_at']  # filter by date
    search_fields = ['content']        # search in content
    ordering_fields = ['created_at']   # order by date
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return JournalEntry.objects.none()
        return JournalEntry.objects.filter(user=user)  # type: ignore
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MoodCheckInListCreateView(generics.ListCreateAPIView):
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['created_at']
    search_fields = ['content']
    ordering_fields = ['created_at']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]    
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return MoodCheckIn.objects.none()
        return MoodCheckIn.objects.filter(user=user)  # type: ignore
    
    def perform_create(self, serializer):
        today = timezone.now().date()
        user = self.request.user
        if MoodCheckIn.objects.filter(user=user, date=today).exists():
            raise ValidationError("You have already submitted a mood check-in for today.")
        serializer.save(user=user, date=today)
        
class DailyTaskListCreateView(generics.ListCreateAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['created_at']
    search_fields = ['content']
    ordering_fields = ['created_at']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return DailyTask.objects.none()
        return DailyTask.objects.filter(user=user)  # type: ignore
    
    def perform_create(self, serializer):
        today = timezone.now().date()
        user = self.request.user
        if DailyTask.objects.filter(user=user, date=today).exists():
            raise ValidationError("You have already created a daily task for today.")
        serializer.save(user=user, date=today)

# Note: Mood analytics are provided by analytics.app at /api/analytics/mood/.
# We intentionally do not duplicate analytics logic here in the journal app.

# Detail views for each model
class JournalEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)  # type: ignore

class MoodCheckInDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MoodCheckInSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MoodCheckIn.objects.filter(user=self.request.user)  # type: ignore

class DailyTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DailyTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DailyTask.objects.filter(user=self.request.user)  # type: ignore

class RitualListCreateView(generics.ListCreateAPIView):
    serializer_class = RitualSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['for_life_phase', 'emotional_tone', 'ritual_type', 'is_for_beginners']
    search_fields = ['title', 'description', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'duration_minutes']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]

    def get_queryset(self):
        return Ritual.objects.filter(is_active=True)
    
class RitualDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RitualSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ritual.objects.filter(is_active=True)
    
# GPT Response View (Updated for Dagi AI)

class GPTAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.conf import settings
        from openai import OpenAI
        import os

        serializer = GPTPromptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prompt = serializer.validated_data['prompt']

        # Initialize OpenAI client
        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        # Check if this is a tarot-related request
        if 'tarot' in prompt.lower() or 'card' in prompt.lower() or 'reading' in prompt.lower():
            return self.handle_tarot_request(request, prompt, client)
        else:
            return self.handle_general_ai_request(request, prompt, client)

    def handle_tarot_request(self, request, prompt, client):
        """Handle tarot-related requests with OpenAI integration"""
        try:
            # Extract tarot reading type from prompt
            prompt_lower = prompt.lower()

            if 'single' in prompt_lower or 'one card' in prompt_lower:
                prompt_type = 'single_card'
                cards_to_draw = 1
            elif 'three' in prompt_lower or 'past present future' in prompt_lower:
                prompt_type = 'three_card'
                cards_to_draw = 3
            elif 'celtic' in prompt_lower or 'cross' in prompt_lower:
                prompt_type = 'celtic_cross'
                cards_to_draw = 10
            elif 'daily' in prompt_lower:
                prompt_type = 'daily'
                cards_to_draw = 1
            else:
                prompt_type = 'custom'
                cards_to_draw = 1

            # Get available tarot cards
            available_cards = TarotCard.objects.filter(is_active=True)
            if available_cards.count() == 0:
                return Response({
                    "error": "No tarot cards available in the system yet."
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # Draw random cards
            drawn_cards = random.sample(list(available_cards), min(cards_to_draw, available_cards.count()))

            # Create card data with positions
            cards_data = []
            for i, card in enumerate(drawn_cards):
                # Randomly decide if card is reversed (20% chance)
                is_reversed = random.random() < 0.2

                card_data = {
                    'card_id': card.id,
                    'name': card.name,
                    'suit': card.suit,
                    'is_major_arcana': card.is_major_arcana,
                    'is_reversed': is_reversed,
                    'position': i,
                    'meanings': card.reversed_meanings if is_reversed else card.upright_meanings
                }
                cards_data.append(card_data)

            # Create enhanced prompt for OpenAI with card details
            card_details = []
            for card in cards_data:
                card_info = TarotCard.objects.get(id=card['card_id'])
                card_details.append({
                    'name': card['name'],
                    'suit': card['suit'],
                    'is_reversed': card['is_reversed'],
                    'meanings': card['meanings']
                })

            # Create OpenAI prompt
            ai_prompt = f"""You are Dagi, a warm and supportive AI tarot reader for women. Provide a gentle, empowering tarot reading.

User's question: {prompt}

Cards drawn:
"""

            for i, card in enumerate(card_details):
                position = self.get_position_name(prompt_type, i)
                ai_prompt += f"{position}: {card['name']} ({card['suit']})"
                if card['is_reversed']:
                    ai_prompt += " - Reversed"
                ai_prompt += f"\nTraditional meanings: {', '.join(card['meanings'][:3])}\n\n"

            ai_prompt += f"""
Please provide a warm, supportive interpretation for this {prompt_type} reading.
Focus on empowerment, growth, and positive guidance.
Keep the tone gentle and encouraging.
Structure your response as:
1. Brief introduction acknowledging the reading type
2. Interpretation for each card in context
3. Overall message and guidance
4. Gentle advice for moving forward

Remember to be supportive and empowering."""

            # Get OpenAI response
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Dagi, a compassionate AI tarot reader focused on women's wellness and empowerment."},
                        {"role": "user", "content": ai_prompt}
                    ],
                    max_tokens=800,
                    temperature=0.7
                )

                interpretation = response.choices[0].message.content.strip()

            except Exception as openai_error:
                # Fallback to basic interpretation if OpenAI fails
                print(f"OpenAI error: {openai_error}")
                interpretation = self.generate_fallback_interpretation(cards_data, prompt_type, prompt)

            # Save the tarot reading
            tarot_reading = TarotPrompt.objects.create(
                user=request.user,
                prompt_type=prompt_type,
                question=prompt,
                cards_drawn=cards_data,
                interpretation=interpretation,
                advice="Take time to reflect on this reading and trust your intuition.",
                is_ai_generated=True,  # Now using real AI
                ai_model_used="gpt-3.5-turbo"
            )

            return Response({
                "message": "Tarot reading completed with AI interpretation",
                "reading": TarotPromptSerializer(tarot_reading).data
            })

        except Exception as e:
            return Response({
                "error": f"Error processing tarot request: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_general_ai_request(self, request, prompt, client):
        """Handle general AI conversation requests with OpenAI"""
        try:
            # Create OpenAI prompt for general conversation
            ai_prompt = f"""You are Dagi, a supportive AI assistant focused on women's wellness, mental health, and personal growth.

User's message: {prompt}

Please provide a warm, supportive, and helpful response. Focus on:
- Emotional support and encouragement
- Practical advice when relevant
- Wellness and self-care suggestions
- Empowerment and positive growth

Keep your response conversational and caring, like a trusted friend."""

            # Get OpenAI response
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Dagi, a compassionate AI assistant focused on women's wellness and empowerment."},
                    {"role": "user", "content": ai_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content.strip()

            # Save the conversation
            conversation = AIConversation.objects.create(
                user=request.user,
                conversation_type='general',
                user_message=prompt,
                ai_response=ai_response,
                context_data={'ai_model': 'gpt-3.5-turbo'},
                is_favorite=False
            )

            return Response({
                "message": "AI response generated",
                "conversation": AIConversationSerializer(conversation).data
            })

        except Exception as e:
            return Response({
                "error": f"Error processing AI request: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_position_name(self, prompt_type, position):
        """Get position name for different reading types"""
        if prompt_type == 'single_card':
            return 'Your Card'

        three_card_positions = ['Past', 'Present', 'Future']
        if position < len(three_card_positions):
            return three_card_positions[position]

        return f'Position {position + 1}'

    def generate_fallback_interpretation(self, cards_data, prompt_type, original_prompt):
        """Generate basic interpretation if OpenAI fails"""
        if prompt_type == 'single_card':
            card = cards_data[0]
            card_obj = TarotCard.objects.get(id=card['card_id'])
            meanings = card['meanings']
            return f"The {card['name']} suggests: {', '.join(meanings[:3])}. Trust your intuition with this guidance."

        elif prompt_type == 'three_card':
            interpretation_parts = []
            positions = ['Past', 'Present', 'Future']

            for i, card in enumerate(cards_data):
                card_obj = TarotCard.objects.get(id=card['card_id'])
                meanings = card['meanings']
                position = positions[i] if i < len(positions) else f'Position {i+1}'
                interpretation_parts.append(f"{position}: {card['name']} - {', '.join(meanings[:2])}")

            return " | ".join(interpretation_parts)

        return "This reading offers you guidance and insight. Take time to reflect on the cards and their meanings."

# Tarot-specific views

class TarotCardListView(generics.ListAPIView):
    """List all available tarot cards"""
    serializer_class = TarotCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TarotCard.objects.filter(is_active=True)

class TarotPromptListCreateView(generics.ListCreateAPIView):
    """List user's tarot readings and create new ones"""
    serializer_class = TarotPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TarotPrompt.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TarotPromptDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific tarot reading"""
    serializer_class = TarotPromptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TarotPrompt.objects.filter(user=self.request.user)

class AIConversationListCreateView(generics.ListCreateAPIView):
    """List user's AI conversations and create new ones"""
    serializer_class = AIConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIConversation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AIConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific AI conversation"""
    serializer_class = AIConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIConversation.objects.filter(user=self.request.user)
