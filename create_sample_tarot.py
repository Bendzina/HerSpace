import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_space.settings')
django.setup()

from journal.models import TarotCard, TarotDeck

def create_sample_tarot_cards():
    """Create sample tarot cards for testing"""

    # Major Arcana cards
    major_arcana_cards = [
        {
            'name': 'The Fool',
            'description': 'New beginnings, innocence, spontaneity, free spirit',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['New beginnings', 'Innocence', 'Spontaneity', 'Free spirit', 'Adventure'],
            'reversed_meanings': ['Recklessness', 'Taken advantage of', 'Inconsideration', 'Foolish behavior']
        },
        {
            'name': 'The Magician',
            'description': 'Manifestation, resourcefulness, power, inspired action',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Manifestation', 'Resourcefulness', 'Power', 'Inspired action', 'Willpower'],
            'reversed_meanings': ['Manipulation', 'Poor planning', 'Untapped talents', 'Lack of focus']
        },
        {
            'name': 'The High Priestess',
            'description': 'Intuition, sacred knowledge, divine feminine, subconscious mind',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Intuition', 'Sacred knowledge', 'Divine feminine', 'Subconscious mind', 'Mystery'],
            'reversed_meanings': ['Secrets', 'Disconnected from intuition', 'Withdrawal', 'Silence']
        },
        {
            'name': 'The Empress',
            'description': 'Femininity, beauty, nature, abundance, mother figure',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Femininity', 'Beauty', 'Nature', 'Abundance', 'Mother figure', 'Nurturing'],
            'reversed_meanings': ['Creative block', 'Dependence on others', 'Smothering', 'Stagnation']
        },
        {
            'name': 'The Emperor',
            'description': 'Authority, establishment, structure, father figure',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Authority', 'Establishment', 'Structure', 'Father figure', 'Stability'],
            'reversed_meanings': ['Domination', 'Excessive control', 'Lack of discipline', 'Inflexibility']
        },
        {
            'name': 'The Lovers',
            'description': 'Love, harmony, relationships, values alignment, choices',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Love', 'Harmony', 'Relationships', 'Values alignment', 'Choices'],
            'reversed_meanings': ['Self-love', 'Disharmony', 'Imbalance', 'Misalignment of values']
        },
        {
            'name': 'The Chariot',
            'description': 'Control, willpower, success, determination, direction',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Control', 'Willpower', 'Success', 'Determination', 'Direction'],
            'reversed_meanings': ['Self-discipline', 'Lack of control', 'Lack of direction', 'Aggression']
        },
        {
            'name': 'Strength',
            'description': 'Strength, courage, persuasion, influence, compassion',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Strength', 'Courage', 'Persuasion', 'Influence', 'Compassion'],
            'reversed_meanings': ['Self-doubt', 'Low energy', 'Raw emotion', 'Lack of confidence']
        },
        {
            'name': 'The Hermit',
            'description': 'Soul searching, introspection, inner guidance, solitude',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Soul searching', 'Introspection', 'Inner guidance', 'Solitude', 'Withdrawal'],
            'reversed_meanings': ['Isolation', 'Loneliness', 'Withdrawal', 'Paranoia']
        },
        {
            'name': 'Wheel of Fortune',
            'description': 'Good luck, karma, life cycles, destiny, turning point',
            'is_major_arcana': True,
            'suit': 'major',
            'upright_meanings': ['Good luck', 'Karma', 'Life cycles', 'Destiny', 'Turning point'],
            'reversed_meanings': ['Bad luck', 'Lack of control', 'Clinging to control', 'Delays']
        }
    ]

    # Minor Arcana - Cups
    cups_cards = [
        {
            'name': 'Ace of Cups',
            'description': 'Love, new relationships, compassion, creativity',
            'is_major_arcana': False,
            'suit': 'cups',
            'upright_meanings': ['Love', 'New relationships', 'Compassion', 'Creativity', 'Emotional fulfillment'],
            'reversed_meanings': ['Self-love', 'Intuition', 'Repressed emotions', 'Emotional withdrawal']
        },
        {
            'name': 'Two of Cups',
            'description': 'Unified love, partnership, mutual attraction, connection',
            'is_major_arcana': False,
            'suit': 'cups',
            'upright_meanings': ['Unified love', 'Partnership', 'Mutual attraction', 'Connection', 'Balance'],
            'reversed_meanings': ['Self-love', 'Break-ups', 'Disharmony', 'Imbalance']
        },
        {
            'name': 'Three of Cups',
            'description': 'Celebration, friendship, creativity, collaborations',
            'is_major_arcana': False,
            'suit': 'cups',
            'upright_meanings': ['Celebration', 'Friendship', 'Creativity', 'Collaborations', 'Community'],
            'reversed_meanings': ['Independence', 'Private celebration', 'Gossip', 'Scandal']
        }
    ]

    # Minor Arcana - Swords
    swords_cards = [
        {
            'name': 'Ace of Swords',
            'description': 'Breakthroughs, new ideas, mental clarity, success',
            'is_major_arcana': False,
            'suit': 'swords',
            'upright_meanings': ['Breakthroughs', 'New ideas', 'Mental clarity', 'Success', 'Truth'],
            'reversed_meanings': ['Inner clarity', 'Re-thinking an idea', 'Clouded judgment', 'Confusion']
        },
        {
            'name': 'Two of Swords',
            'description': 'Difficult decisions, weighing up options, avoidance',
            'is_major_arcana': False,
            'suit': 'swords',
            'upright_meanings': ['Difficult decisions', 'Weighing up options', 'Avoidance', 'Stalemate', 'Mediation'],
            'reversed_meanings': ['Inner turmoil', 'Indecision', 'Confusion', 'Information overload']
        }
    ]

    # Minor Arcana - Pentacles
    pentacles_cards = [
        {
            'name': 'Ace of Pentacles',
            'description': 'New financial opportunity, manifestation, abundance',
            'is_major_arcana': False,
            'suit': 'pentacles',
            'upright_meanings': ['New financial opportunity', 'Manifestation', 'Abundance', 'Prosperity', 'Security'],
            'reversed_meanings': ['Lost opportunity', 'Missed chance', 'Bad investment', 'Financial delays']
        },
        {
            'name': 'Two of Pentacles',
            'description': 'Multiple priorities, time management, prioritization',
            'is_major_arcana': False,
            'suit': 'pentacles',
            'upright_meanings': ['Multiple priorities', 'Time management', 'Prioritization', 'Adaptability', 'Balance'],
            'reversed_meanings': ['Over-committed', 'Disorganisation', 'Reprioritisation', 'Financial stress']
        }
    ]

    # Minor Arcana - Wands
    wands_cards = [
        {
            'name': 'Ace of Wands',
            'description': 'Inspiration, new opportunities, growth, potential',
            'is_major_arcana': False,
            'suit': 'wands',
            'upright_meanings': ['Inspiration', 'New opportunities', 'Growth', 'Potential', 'Action'],
            'reversed_meanings': ['An emerging idea', 'Lack of direction', 'Distractions', 'Delays']
        },
        {
            'name': 'Two of Wands',
            'description': 'Future planning, progress, decisions, discovery',
            'is_major_arcana': False,
            'suit': 'wands',
            'upright_meanings': ['Future planning', 'Progress', 'Decisions', 'Discovery', 'Partnership'],
            'reversed_meanings': ['Personal goals', 'Inner alignment', 'Fear of unknown', 'Lack of planning']
        }
    ]

    # Combine all cards
    all_cards_data = major_arcana_cards + cups_cards + swords_cards + pentacles_cards + wands_cards

    # Create cards
    created_count = 0
    for card_data in all_cards_data:
        card, created = TarotCard.objects.get_or_create(
            name=card_data['name'],
            defaults=card_data
        )
        if created:
            created_count += 1

    print(f"Created {created_count} new tarot cards")

    # Create a default deck
    default_deck, deck_created = TarotDeck.objects.get_or_create(
        name='Rider-Waite-Smith',
        defaults={
            'description': 'The classic Rider-Waite-Smith tarot deck',
            'is_active': True
        }
    )

    if deck_created:
        # Add all cards to the default deck
        all_cards = TarotCard.objects.all()
        default_deck.cards.set(all_cards)
        print(f"Created default deck '{default_deck.name}' with {all_cards.count()} cards")

    print(f"Total tarot cards in system: {TarotCard.objects.count()}")
    print(f"Total tarot decks in system: {TarotDeck.objects.count()}")

if __name__ == '__main__':
    create_sample_tarot_cards()
