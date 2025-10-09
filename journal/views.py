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

        print(f"🔵 === DAGI AI REQUEST ===")
        print(f"🔵 User: {request.user.username}")
        print(f"🔵 Prompt: {prompt}")

        # Initialize OpenAI client
        try:
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            print(f"✅ OpenAI client initialized")
        except Exception as e:
            print(f"❌ Error initializing OpenAI client: {str(e)}")
            return Response({
                "error": f"Failed to initialize AI service: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Check if this is a tarot-related request
        if 'tarot' in prompt.lower() or 'card' in prompt.lower() or 'reading' in prompt.lower():
            print(f"🔮 Detected TAROT request")
            return self.handle_tarot_request(request, prompt, client)
        else:
            print(f"💬 Detected GENERAL request")
            return self.handle_general_ai_request(request, prompt, client)

    def handle_tarot_request(self, request, prompt, client):
        """Handle tarot-related requests with OpenAI integration"""
        try:
            print(f"🔮 Processing tarot request...")
            
            # Extract tarot reading type from prompt
            prompt_lower = prompt.lower()
            
            # Check if the prompt is in Georgian
            is_georgian = any('ა' <= char <= 'ჿ' for char in prompt)
            print(f"🔤 Language detected: {'Georgian' if is_georgian else 'Non-Georgian'}")

            # Try to extract numeric card count from prompt (e.g., "Draw 3 cards" or "five card spread")
            import re
            numeric_match = re.search(r'\b(\d+)\s*card', prompt_lower)
            if not numeric_match:
                # Also match patterns like "five card spread", "three card", etc.
                word_to_number = {
                    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
                    'ერთი': 1, 'ორი': 2, 'სამი': 3, 'ოთხი': 4, 'ხუთი': 5
                }
                for word, number in word_to_number.items():
                    if word in prompt_lower:
                        cards_to_draw = number
                        break
                else:
                    cards_to_draw = 1
            else:
                cards_to_draw = int(numeric_match.group(1))

            if cards_to_draw == 1:
                prompt_type = 'single_card'
            elif cards_to_draw == 3:
                prompt_type = 'three_card'
            elif cards_to_draw == 10:
                prompt_type = 'celtic_cross'
            elif cards_to_draw == 5:
                prompt_type = 'five_card'
            else:
                prompt_type = 'custom'

            print(f"🔮 Reading type: {prompt_type}, Cards to draw: {cards_to_draw}")

            # Get available tarot cards
            available_cards = TarotCard.objects.filter(is_active=True)
            print(f"🔮 Available cards in database: {available_cards.count()}")
            
            if available_cards.count() == 0:
                return Response({
                    "error": "No tarot cards available in the system yet. Please run create_sample_tarot_cards.py"
                }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

            # Draw random cards
            drawn_cards = random.sample(list(available_cards), min(cards_to_draw, available_cards.count()))
            print(f"🔮 Drew {len(drawn_cards)} cards")

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
                print(f"🔮 Card {i+1}: {card.name} {'(Reversed)' if is_reversed else ''}")

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

            # Check if the prompt is in Georgian
            is_georgian = any('\u10D0' <= char <= '\u10FF' for char in prompt)
            
            # Create language-specific prompts
            if is_georgian:
                ai_prompt = """
                თქვენ ხართ დაგი, თბილი და მხარდამჭერი ტაროს მკითხაური ქალებისთვის. 
                მოგაწვდით ტაროს გაშლის თბილ, გულწრფელ ინტერპრეტაციას.

                მომხმარებლის შეკითხვა: {prompt}

                გაშლილი კარტები:
                """

                for i, card in enumerate(card_details):
                    position = self.get_position_name_georgian(prompt_type, i)
                    ai_prompt += f"{i+1}. {position}: {card['name']} ({card['suit']})"
                    if card['is_reversed']:
                        ai_prompt += " - შებრუნებული"
                    ai_prompt += f"\nტრადიციული მნიშვნელობები: {', '.join(card['meanings'][:3])}\n\n"

                ai_prompt += """
                გთხოვთ, მოგაწოდოთ თბილი, მხარდამჭერი ინტერპრეტაცია ამ ტაროს გაშლისთვის.
                ფოკუსირება გაძლიერებაზე, ზრდასა და დადებით ხელმძღვანელობაზე.
                შეინარჩუნეთ თბილი და მხარდამჭერი ტონი.

                პასუხის სტრუქტურა:
                1. მოკლე შესავალი, რომელშიც აღნიშნულია გაშლის ტიპი
                2. თითოეული კარტის დეტალური ინტერპრეტაცია მათი პოზიციის კონტექსტში (კარტები უნდა იყოს დანომრილი: 1-ლი კარტი, 2-ლი კარტი, და ა.შ.)
                3. ზოგადი შეტყობინება და ხელმძღვანელობა, რომელიც აკავშირებს ყველა კარტს
                4. რჩევები შემდგომი მოქმედებისთვის

                ᲛᲜᲘᲨᲕᲜᲔᲚᲝᲕᲐᲜᲘᲐ: თქვენი მთელი პასუხი უნდა იყოს ქართულად!
                იყავით მხარდამჭერი და გამაძლიერებელი.
                ᲛᲜᲘᲨᲕᲜᲔᲚᲝᲕᲐᲜᲘᲐ: მომხმარებლის მიერ დასმული შეკითხვის მიხედვით, ტაროს კარტების ინტერპრეტაციის დროს უნდა დაიწეროს შესაბამისი რჩევები.
"""
            else:
                ai_prompt = f"""You are Dagi, a warm and supportive AI tarot reader for women. Provide a gentle, empowering tarot reading.

                User's question: {prompt}

                Cards drawn:
                """

                for i, card in enumerate(card_details):
                    position = self.get_position_name(prompt_type, i)
                    ai_prompt += f"{i+1}. {position}: {card['name']} ({card['suit']})"
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

                Remember to be supportive and empowering.
                """

            # Get OpenAI response
            try:
                print(f"🔮 Calling OpenAI API...")
                
                # Use language-specific system message
                if is_georgian:
                    system_message = "თქვენ ხართ დაგი, თბილი და თანაგრძნობიანი ტაროს მკითხველი ქალების ჯანმრთელობისა და გაძლიერებაზე ორიენტირებული. პასუხი გაეცით მხოლოდ ქართულად."
                else:
                    system_message = "You are Dagi, a compassionate AI tarot reader focused on women's wellness and empowerment."
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # Better multilingual support than gpt-3.5-turbo
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": ai_prompt}
                    ],
                    max_tokens=1500,
                    temperature=0.7
                )

                interpretation = response.choices[0].message.content.strip()
                print(f"✅ OpenAI response received: {len(interpretation)} characters")

            except Exception as openai_error:
                # Fallback to basic interpretation if OpenAI fails
                print(f"❌ OpenAI error: {openai_error}")
                print(f"🔮 Using fallback interpretation...")
                interpretation = self.generate_fallback_interpretation(cards_data, prompt_type, prompt)

            # Save the tarot reading
            tarot_reading = TarotPrompt.objects.create(
                user=request.user,
                prompt_type=prompt_type,
                question=prompt,
                cards_drawn=cards_data,
                interpretation=interpretation,
                advice="Take time to reflect on this reading and trust your intuition.",
                is_ai_generated=True,
                ai_model_used="gpt-4o-mini"
            )

            print(f"✅ Tarot reading saved with ID: {tarot_reading.id}")
            print(f"🔵 === END TAROT REQUEST ===\n")

            # ✅ FIX: Return interpretation as message
            reading_data = TarotPromptSerializer(tarot_reading).data

            return Response({
                "message": interpretation,  # ✅ აქ უნდა იყოს interpretation!
                "reading": reading_data,
                "temporary_note": "🔮 Tarot reading completed"
            })

        except Exception as e:
            print(f"❌ Error in handle_tarot_request: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                "error": f"Error processing tarot request: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def handle_general_ai_request(self, request, prompt, client):
        """Handle general AI conversation requests with OpenAI"""
        try:
            print(f"💬 Processing general AI request...")
            
            # Detect language for response
            is_georgian = any('\u10D0' <= char <= '\u10FF' for char in prompt)
            
            # Set system message based on language
            if is_georgian:
                system_message = """თქვენ ხართ დაგი, თბილი და მხარდამჭერი ხელოვანი ინტელექტი ქალებისთვის. 
                გთხოვთ, პასუხი გაეცით მხოლოდ ქართულად. იყავით თბილი, მხარდამჭერი და გულწრფელი.
                ყურადღება მიაქციეთ:
                - ემოციურ მხარდაჭერას
                - პრაქტიკულ რჩევებს
                - კეთილდღეობისა და თვითზრუნვის წინადადებებს
                - გაძლიერებასა და დადებით ცვლილებებს"""
            else:
                system_message = """You are Dagi, a warm and supportive AI assistant for women. 
                Please respond in English. Be caring, supportive, and genuine.
                Focus on:
                - Emotional support
                - Practical advice
                - Wellness and self-care suggestions
                - Empowerment and positive growth"""

            # Get OpenAI response
            print(f"💬 Calling OpenAI API...")
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Using the same model as tarot for consistency
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content.strip()
            print(f"✅ OpenAI response received: {len(ai_response)} characters")

            # Save the conversation
            conversation = AIConversation.objects.create(
                user=request.user,
                conversation_type='general',
                user_message=prompt,
                ai_response=ai_response,
                context_data={'ai_model': 'gpt-4o-mini'},  # Updated to match the model being used
                is_favorite=False
            )

            print(f"✅ Conversation saved with ID: {conversation.id}")
            print(f"🔵 === END GENERAL REQUEST ===\n")

            # ✅ FIX: Return ai_response as message
            return Response({
                "message": ai_response,  # ✅ აქ უნდა იყოს ai_response!
                "conversation": AIConversationSerializer(conversation).data,
                "temporary_note": "✨ Powered by AI"
            })

        except Exception as e:
            print(f"❌ Error in handle_general_ai_request: {str(e)}")
            import traceback
            traceback.print_exc()
            return Response({
                "error": f"Error processing AI request: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_position_name(self, prompt_type, position):
        """Get position name for different reading types in English"""
        if prompt_type == 'single_card':
            return 'Your Card'

        three_card_positions = ['Past', 'Present', 'Future']
        if prompt_type == 'three_card' and position < len(three_card_positions):
            return three_card_positions[position]

        five_card_positions = ['Past', 'Present', 'Challenge', 'Outcome', 'Advice']
        if prompt_type == 'five_card' and position < len(five_card_positions):
            return five_card_positions[position]

        celtic_cross_positions = [
            'The Present / The Self', 'The Challenge', 'The Past', 'The Future (Near)',
            'Above / Conscious', 'Below / Subconscious', 'Advice / Self',
            'External Influences', 'Hopes & Fears', 'Outcome'
        ]
        if prompt_type == 'celtic_cross' and position < len(celtic_cross_positions):
            return celtic_cross_positions[position]

        return f'Position {position + 1}'
        
    def get_position_name_georgian(self, prompt_type, position):
        """Get position name for different reading types in Georgian"""
        if prompt_type == 'single_card':
            return 'თქვენი კარტი'
            
        three_card_positions = ['წარსული', 'აწმყო', 'მომავალი']
        if prompt_type == 'three_card' and position < len(three_card_positions):
            return three_card_positions[position]
            
        five_card_positions = ['წარსული', 'აწმყო', 'გამოწვევა', 'შედეგი', 'რჩევა']
        if prompt_type == 'five_card' and position < len(five_card_positions):
            return five_card_positions[position]
            
        celtic_cross_positions = [
            'აწმყო / საკუთარი თავი', 'გამოწვევა', 'წარსული', 'მომავალი (ახლო)',
            'ზემოთ / ცნობიერება', 'ქვემოთ / ქვეცნობიერება', 'რჩევა / საკუთარი თავი',
            'გარე გავლენები', 'იმედები და შიშები', 'შედეგი'
        ]
        if prompt_type == 'celtic_cross' and position < len(celtic_cross_positions):
            return celtic_cross_positions[position]
            
        return f'პოზიცია {position + 1}'

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