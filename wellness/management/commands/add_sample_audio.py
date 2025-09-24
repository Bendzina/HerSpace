import os
import random
from django.core.files import File
from django.core.management.base import BaseCommand
from wellness.models import MindfulnessActivity

class Command(BaseCommand):
    help = 'Adds sample audio files to mindfulness activities'

    def create_sample_audio_file(self, filename, duration_minutes):
        """Create a silent MP3 file of the specified duration."""
        os.makedirs('media/mindfulness/audio', exist_ok=True)
        audio_path = f'media/mindfulness/audio/{filename}'
        
        # Create a silent MP3 file with appropriate duration
        # This is a minimal MP3 header followed by silent frames
        # Note: This creates a very small file that will play as silence
        with open(audio_path, 'wb') as f:
            # ID3 header
            f.write(b'ID3\x03\x00\x00\x00\x00\x00\x00')
            
            # Add some silent frames (each frame is 26 bytes for 8kbps mono MP3)
            # At 8kbps, 1 second ≈ 1KB
            silent_frame = b'\xff\xfb\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            frames_per_second = 38  # 8kbps MP3 has ~38 frames per second
            for _ in range(frames_per_second * duration_minutes * 60):
                f.write(silent_frame)
        
        return audio_path

    def handle(self, *args, **options):
        # Sample audio descriptions based on activity type
        audio_descriptions = {
            'breathing': {
                'prefix': 'breathing',
                'titles': [
                    'Guided Deep Breathing',
                    'Calm Breathing Exercise',
                    'Mindful Breathing Practice'
                ]
            },
            'meditation': {
                'prefix': 'meditation',
                'titles': [
                    'Guided Body Scan',
                    'Mindfulness Meditation',
                    'Loving-Kindness Practice'
                ]
            },
            'gratitude': {
                'prefix': 'gratitude',
                'titles': [
                    'Gratitude Reflection',
                    'Thankfulness Practice',
                    'Appreciation Meditation'
                ]
            }
        }

        # Process all active mindfulness activities
        activities = MindfulnessActivity.objects.filter(is_active=True)
        
        if not activities.exists():
            self.stdout.write(self.style.WARNING('No active mindfulness activities found.'))
            return

        for activity in activities:
            # Skip if already has an audio file
            if activity.audio_file:
                self.stdout.write(self.style.WARNING(f'Skipping "{activity.title}" - already has an audio file'))
                continue

            # Get appropriate audio description based on category
            category = activity.category or 'meditation'
            audio_info = audio_descriptions.get(category, audio_descriptions['meditation'])
            
            # Generate a unique filename
            filename = f"{audio_info['prefix']}_{activity.id}_{random.randint(1000, 9999)}.mp3"
            
            try:
                # Create a sample audio file with appropriate duration
                audio_path = self.create_sample_audio_file(
                    filename=filename,
                    duration_minutes=activity.duration_minutes or 5
                )
                
                # Add the audio file to the activity
                with open(audio_path, 'rb') as f:
                    activity.audio_file.save(filename, File(f), save=True)
                
                # Update the description with more details if it's a default one
                if not activity.short_description or 'sample' in activity.short_description.lower():
                    activity.short_description = random.choice(audio_info['titles'])
                    activity.save()
                
                self.stdout.write(self.style.SUCCESS(
                    f'Added sample audio to activity: "{activity.title}" '
                    f'({activity.duration_minutes} min, {os.path.getsize(audio_path) / 1024:.1f}KB)'
                ))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f'Error adding audio to "{activity.title}": {str(e)}'
                ))
        
        self.stdout.write(self.style.SUCCESS('Finished processing all activities'))
