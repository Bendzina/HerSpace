import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_space.settings')
django.setup()

from journal.models import Ritual

def create_sample_rituals():
    rituals = [
        # Morning Gratitude - English
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
            'is_active': True,
            'language': 'en'
        },
        # Morning Gratitude - Georgian
        {
            'title': 'დილის მადლიერება',
            'description': 'დაიწყეთ დღე მადლიერებით და დადებითი ენერგიით',
            'ritual_type': 'affirmation',
            'content': 'მე ვარ მადლიერი ამ ახალი დღისთვის და ყველა შესაძლებლობისთვის, რასაც ის მოაქვს.',
            'for_life_phase': 'any',
            'emotional_tone': 'gentle',
            'duration_minutes': 5,
            'is_for_beginners': True,
            'tags': ['morning', 'gratitude'],
            'is_active': True,
            'language': 'ka'
        },
        
        # Evening Reflection - English
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
            'is_active': True,
            'language': 'en'
        },
        # Evening Reflection - Georgian
        {
            'title': 'საღამოს ასახვა',
            'description': 'დაფიქრდით დღეზე და იპოვეთ მადლიერების მომენტები',
            'ritual_type': 'prompt',
            'content': 'რა იყო სამი რამ, რაც დღეს სიამოვნება მოგაგინათ?',
            'for_life_phase': 'any',
            'emotional_tone': 'gentle',
            'duration_minutes': 10,
            'is_for_beginners': True,
            'tags': ['evening', 'reflection'],
            'is_active': True,
            'language': 'ka'
        },
        
        # Breath Awareness - English
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
            'is_active': True,
            'language': 'en'
        },
        # Breath Awareness - Georgian
        {
            'title': 'სუნთქვის ცნობიერება',
            'description': 'მარტივი მედიტაცია თავის ცენტრირებისთვის',
            'ritual_type': 'meditation',
            'content': 'ფოკუსირდით თქვენს სუნთქვაზე. ჩაისუნთქეთ 4-ჯერ, დაიჭირეთ 4-ზე, ამოისუნთქეთ 6-ზე.',
            'for_life_phase': 'transition',
            'emotional_tone': 'grounding',
            'duration_minutes': 7,
            'is_for_beginners': True,
            'tags': ['breathing', 'meditation'],
            'is_active': True,
            'language': 'ka'
        },
        
        # Self-Love Affirmation - English
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
            'is_active': True,
            'language': 'en'
        },
        # Self-Love Affirmation - Georgian
        {
            'title': 'თვით-სიყვარულის აფირმაცია',
            'description': 'გაზარდეთ თქვენი თვითშეფასება დადებითი აფირმაციებით',
            'ritual_type': 'affirmation',
            'content': 'მე საკმარისად კარგი ვარ. მე ვიმსახურებ სიყვარულს და პატივისცემას.',
            'for_life_phase': 'healing',
            'emotional_tone': 'empowering',
            'duration_minutes': 5,
            'is_for_beginners': True,
            'tags': ['self-love', 'affirmations'],
            'is_active': True,
            'language': 'ka'
        },
        
        # Motherhood Moments - English
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
            'is_active': True,
            'language': 'en'
        },
        # Motherhood Moments - Georgian
        {
            'title': 'დედობის მომენტები',
            'description': 'დაფიქრდით თქვენს დედობის გზაზე',
            'ritual_type': 'prompt',
            'content': 'რომელი იყო დღის ის მომენტი, რომელმაც შემოგახსენათ დედობის სილამაზე?',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'gentle',
            'duration_minutes': 8,
            'is_for_beginners': True,
            'tags': ['motherhood', 'reflection', 'gratitude'],
            'is_active': True,
            'language': 'ka'
        },
        
        # Self-Care for Moms - English
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
            'is_active': True,
            'language': 'en'
        },
        # Self-Care for Moms - Georgian
        {
            'title': 'დედების თვითზრუნვა',
            'description': 'სწრაფი შეხსენება დაკავებული დედებისთვის',
            'ritual_type': 'affirmation',
            'content': 'მე ვცემ უპირატესობას ჩემს საჭიროებებს, რადგან მეც ვიმსახურებ ზრუნვას. ჩემთვის დროის გამოყოფა უკეთეს დედად ხდის.',
            'for_life_phase': 'motherhood',
            'emotional_tone': 'healing',
            'duration_minutes': 5,
            'is_for_beginners': True,
            'tags': ['motherhood', 'self-care', 'affirmation'],
            'is_active': True,
            'language': 'ka'
        }
    ]

    count = 0
    for ritual_data in rituals:
        try:
            # Create a copy of the data to avoid modifying the original
            ritual_data_copy = ritual_data.copy()
            language = ritual_data_copy.pop('language', 'en')
            
            # Create or update the ritual with the language field
            ritual, created = Ritual.objects.update_or_create(
                title=ritual_data['title'],
                language=language,
                defaults=ritual_data_copy
            )
            
            if created:
                count += 1
                print(f'✅ Created ritual ({language}): {ritual.title}')
            else:
                print(f'↩️  Updated ritual ({language}): {ritual.title}')
                
        except Exception as e:
            print(f'❌ Error creating ritual {ritual_data.get("title", "Unknown")}: {str(e)}')

    print(f'Successfully loaded {count} rituals')

if __name__ == '__main__':
    create_sample_rituals()
