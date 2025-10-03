import os
import django
import random
from datetime import time, timedelta
from django.utils import timezone

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_space.settings')
    django.setup()

    from django.contrib.auth import get_user_model
    from motherhood.models import ChildcareRoutine, MotherhoodResource, MotherhoodJournal, SupportGroup

    User = get_user_model()
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testmother',
        defaults={
            'email': 'mother@example.com',
            'first_name': 'Test',
            'last_name': 'Mother'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()

    # Sample Childcare Routines
    routine_types = ['feeding', 'sleep', 'play', 'hygiene', 'medical', 'other']
    routine_titles = [
        'Morning Feeding', 'Nap Time', 'Play Time', 'Bath Time',
        'Dinner Time', 'Bedtime Routine', 'Medication', 'Outdoor Play'
    ]
    
    routines = []
    for i, title in enumerate(routine_titles):
        routine = ChildcareRoutine.objects.create(
            user=user,
            title=title,
            routine_type=random.choice(routine_types),
            description=f"Sample {title.lower()} routine description",
            time_of_day=time(hour=random.randint(6, 20), minute=0),
            duration_minutes=random.choice([15, 30, 45, 60]),
            is_active=True
        )
        routines.append(routine)

    # Sample Motherhood Resources
    resource_types = ['article', 'video', 'podcast', 'book', 'app', 'community', 'professional']
    resource_categories = [
        'pregnancy', 'newborn', 'toddler', 'preschool', 
        'school_age', 'teen', 'self_care', 'relationships', 
        'mental_health', 'work_life'
    ]
    
    resource_titles = [
        'The First 40 Days: A Guide to New Motherhood',
        'Gentle Sleep Training Methods',
        'Nutrition for Nursing Mothers',
        'Balancing Work and Motherhood',
        'Postpartum Mental Health Resources',
        'Toddler Discipline That Works',
        'Self-Care for Busy Moms',
        'Building Strong Family Bonds'
    ]
    
    for i, title in enumerate(resource_titles):
        MotherhoodResource.objects.create(
            title=title,
            resource_type=random.choice(resource_types),
            category=random.choice(resource_categories),
            description=f"A comprehensive guide about {title.lower()}",
            url=f"https://example.com/resources/{title.lower().replace(' ', '-')}",
            author=f"Author {i+1}",
            is_featured=random.choice([True, False]),
            is_active=True
        )

    # Sample Motherhood Journal Entries
    moods = ['overwhelmed', 'joyful', 'exhausted', 'grateful', 'frustrated', 'proud', 'anxious', 'peaceful']
    for i in range(5):
        MotherhoodJournal.objects.create(
            user=user,
            title=f"Journal Entry {i+1}",
            content=f"Today was {'a good' if i % 2 == 0 else 'a challenging'} day. " \
                   f"I felt {random.choice(['happy with my progress', 'a bit overwhelmed', 'grateful for small moments', 'tired but accomplished'])}.",
            mood=random.choice(moods),
            is_private=random.choice([True, False])
        )

    # Sample Support Groups
    group_types = ['pregnancy', 'newborn', 'single_mom', 'working_mom', 'mental_health', 'general']
    group_names = [
        'New Moms Support Circle',
        'Working Mothers Network',
        'Single Moms United',
        'Postpartum Support Group',
        'Mindful Parenting Community'
    ]
    
    for name in group_names:
        SupportGroup.objects.create(
            name=name,
            group_type=random.choice(group_types),
            description=f"A supportive community for {name.lower()}",
            is_private=random.choice([True, False]),
            max_members=random.randint(10, 50),
            current_members=random.randint(0, 30),
            is_active=True
        )

    print("✅ Successfully added sample motherhood data!")

if __name__ == "__main__":
    main()
