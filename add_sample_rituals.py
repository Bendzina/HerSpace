import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_space.settings')
django.setup()

from journal.models import Ritual

def create_sample_rituals():
    rituals = [
        # General Rituals
        {
            'title': 'Morning Gratitude',
            'description': 'Start your day with gratitude and positive energy',
            'ritual_type': 'affirmation',
            'content': 'I am grateful for this new day and all the opportunities it brings.',
            'for_life_phase': 'any',
            'emotional_tone': 'gentle',
            'duration_minutes': 5,
            'is_for_beginners': True,
            'tags': ['morning', 'gratitude'],
            'is_active': True
        },
        {
            'title': 'Evening Reflection',
            'description': 'Reflect on your day and find moments of gratitude',
            'ritual_type': 'prompt',
            'content': 'What were three things that brought you joy today?',
            'for_life_phase': 'any',
            'emotional_tone': 'gentle',
            'duration_minutes': 10,
            'is_for_beginners': True,
            'tags': ['evening', 'reflection'],
            'is_active': True
        },
        {
            'title': 'Breath Awareness',
            'description': 'A simple meditation to center yourself',
            'ritual_type': 'meditation',
            'content': 'Focus on your breath. Inhale for 4 counts, hold for 4, exhale for 6.',
            'for_life_phase': 'transition',
            'emotional_tone': 'grounding',
            'duration_minutes': 7,
            'is_for_beginners': True,
            'tags': ['breathing', 'meditation'],
            'is_active': True
        },
        {
            'title': 'Self-Love Affirmation',
            'description': 'Boost your self-esteem with positive affirmations',
            'ritual_type': 'affirmation',
            'content': 'I am enough. I am worthy of love and respect.',
            'for_life_phase': 'healing',
            'emotional_tone': 'empowering',
            'duration_minutes': 5,
            'is_for_beginners': True,
            'tags': ['self-love', 'affirmations'],
            'is_active': True
        },
        {
            'title': 'Daily Intention',
            'description': 'Set your intention for the day',
            'ritual_type': 'prompt',
            'content': 'What is one thing you want to accomplish today?',
            'for_life_phase': 'any',
            'emotional_tone': 'uplifting',
            'duration_minutes': 3,
            'is_for_beginners': True,
            'tags': ['intention', 'morning'],
            'is_active': True
        },
        
        # Motherhood-Specific Rituals
        {
            'title': 'Motherhood Moments',
            'description': 'Reflect on your motherhood journey',
            'ritual_type': 'prompt',
            'content': 'What is one moment today that reminded you of the beauty of motherhood?',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'gentle',
            'duration_minutes': 8,
            'is_for_beginners': True,
            'tags': ['motherhood', 'reflection', 'gratitude'],
            'is_active': True
        },
        {
            'title': 'Self-Care for Moms',
            'description': 'A quick self-care reminder for busy moms',
            'ritual_type': 'affirmation',
            'content': 'I honor my needs because I deserve care too. Taking time for myself makes me a better mother.',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'healing',
            'duration_minutes': 5,
            'is_for_beginners': True,
            'tags': ['motherhood', 'self-care', 'affirmation'],
            'is_active': True
        },
        {
            'title': 'Bedtime Gratitude with Kids',
            'description': 'A family gratitude practice',
            'ritual_type': 'prompt',
            'content': 'Share one thing you\'re grateful for about each family member today.',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'uplifting',
            'duration_minutes': 10,
            'is_for_beginners': True,
            'tags': ['motherhood', 'family', 'gratitude', 'evening'],
            'is_active': True
        },
        {
            'title': 'Mindful Parenting Pause',
            'description': 'A quick mindfulness exercise for challenging moments',
            'ritual_type': 'meditation',
            'content': 'When feeling overwhelmed, take 3 deep breaths. With each breath, silently say: "This moment is hard. I am doing my best. I am enough."',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'grounding',
            'duration_minutes': 3,
            'is_for_beginners': True,
            'tags': ['motherhood', 'mindfulness', 'parenting'],
            'is_active': True
        },
        {
            'title': 'Motherhood Milestones',
            'description': 'Celebrate your growth as a mother',
            'ritual_type': 'prompt',
            'content': 'What is one way you\'ve grown as a mother this week?',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'empowering',
            'duration_minutes': 7,
            'is_for_beginners': True,
            'tags': ['motherhood', 'growth', 'reflection'],
            'is_active': True
        }
    ]

    count = 0
    for ritual_data in rituals:
        ritual, created = Ritual.objects.update_or_create(
            title=ritual_data['title'],
            defaults=ritual_data
        )
        if created:
            count += 1
            print(f'Created ritual: {ritual.title}')
        else:
            print(f'Updated ritual: {ritual.title}')

    print(f'Successfully loaded {count} rituals')

if __name__ == '__main__':
    create_sample_rituals()
