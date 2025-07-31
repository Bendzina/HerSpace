from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import UserInsight
from .serializers import (
    UserInsightSerializer, MoodAnalyticsSerializer, 
    TaskAnalyticsSerializer, JournalAnalyticsSerializer
)
from journal.models import JournalEntry, MoodCheckIn, DailyTask

class MoodAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        days = int(request.query_params.get('days', 30))
        
        # Get mood data for the specified period
        start_date = timezone.now().date() - timedelta(days=days)
        mood_data = MoodCheckIn.objects.filter(
            user=user, 
            date__gte=start_date
        ).order_by('date')
        
        # Calculate analytics
        total_checkins = mood_data.count()
        
        if total_checkins == 0:
            return Response({
                'total_checkins': 0,
                'mood_distribution': {},
                'most_common_mood': 'No data',
                'average_mood_score': 0,
                'mood_trend': []
            })
        
        # Mood distribution
        mood_distribution = mood_data.values('mood').annotate(count=Count('mood'))
        mood_dist = {item['mood']: item['count'] for item in mood_distribution}
        
        # Most common mood
        most_common_mood = max(mood_dist.items(), key=lambda x: x[1])[0]
        
        # Mood scoring (simple scoring system)
        mood_scores = {'happy': 4, 'calm': 3, 'anxious': 2, 'sad': 1}
        total_score = sum(mood_scores.get(mood.mood, 0) for mood in mood_data)
        average_mood_score = total_score / total_checkins
        
        # Mood trend (last 7 days)
        recent_moods = mood_data.filter(date__gte=timezone.now().date() - timedelta(days=7))
        mood_trend = [{'date': str(mood.date), 'mood': mood.mood} for mood in recent_moods]
        
        data = {
            'total_checkins': total_checkins,
            'mood_distribution': mood_dist,
            'most_common_mood': most_common_mood,
            'average_mood_score': round(average_mood_score, 2),
            'mood_trend': mood_trend
        }
        
        # Store insight
        UserInsight.objects.update_or_create(
            user=user,
            insight_type='mood_pattern',
            defaults={'data': data}
        )
        
        serializer = MoodAnalyticsSerializer(data)
        return Response(serializer.data)

class TaskAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        days = int(request.query_params.get('days', 30))
        
        # Get task data for the specified period
        start_date = timezone.now().date() - timedelta(days=days)
        task_data = DailyTask.objects.filter(
            user=user, 
            date__gte=start_date
        )
        
        total_tasks = task_data.count()
        completed_tasks = task_data.filter(completed=True).count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Task completion trend (last 7 days)
        recent_tasks = task_data.filter(date__gte=timezone.now().date() - timedelta(days=7))
        task_trend = []
        for i in range(7):
            date = timezone.now().date() - timedelta(days=i)
            day_tasks = recent_tasks.filter(date=date)
            completed = day_tasks.filter(completed=True).count()
            total = day_tasks.count()
            task_trend.append({
                'date': str(date),
                'completed': completed,
                'total': total,
                'rate': (completed / total * 100) if total > 0 else 0
            })
        task_trend.reverse()
        
        # Most completed task type (simplified)
        most_completed_task_type = 'body_task'  # This could be enhanced with more analysis
        
        data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': round(completion_rate, 2),
            'task_completion_trend': task_trend,
            'most_completed_task_type': most_completed_task_type
        }
        
        # Store insight
        UserInsight.objects.update_or_create(
            user=user,
            insight_type='task_completion',
            defaults={'data': data}
        )
        
        serializer = TaskAnalyticsSerializer(data)
        return Response(serializer.data)

class JournalAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        days = int(request.query_params.get('days', 30))
        
        # Get journal data for the specified period
        start_date = timezone.now().date() - timedelta(days=days)
        journal_data = JournalEntry.objects.filter(
            user=user, 
            created_at__date__gte=start_date
        )
        
        total_entries = journal_data.count()
        
        if total_entries == 0:
            return Response({
                'total_entries': 0,
                'average_entries_per_week': 0,
                'most_active_day': 'No data',
                'entry_length_stats': {},
                'journaling_streak': 0
            })
        
        # Average entries per week
        weeks = max(days / 7, 1)
        average_entries_per_week = total_entries / weeks
        
        # Most active day of week
        day_counts = journal_data.extra(
            select={'day': 'EXTRACT(dow FROM created_at)'}
        ).values('day').annotate(count=Count('id'))
        
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        if day_counts:
            max_day = max(day_counts, key=lambda x: x['count'])
            day_index = int(max_day['day'])  # Convert Decimal to int
            most_active_day = days_of_week[day_index]
        else:
            most_active_day = 'No data'
        
        # Entry length statistics
        entry_lengths = [len(entry.content) for entry in journal_data]
        entry_length_stats = {
            'average_length': round(sum(entry_lengths) / len(entry_lengths)),
            'shortest': min(entry_lengths),
            'longest': max(entry_lengths)
        }
        
        # Journaling streak (simplified)
        journaling_streak = 0
        current_date = timezone.now().date()
        for i in range(30):  # Check last 30 days
            check_date = current_date - timedelta(days=i)
            if journal_data.filter(created_at__date=check_date).exists():
                journaling_streak += 1
            else:
                break
        
        data = {
            'total_entries': total_entries,
            'average_entries_per_week': round(average_entries_per_week, 2),
            'most_active_day': most_active_day,
            'entry_length_stats': entry_length_stats,
            'journaling_streak': journaling_streak
        }
        
        # Store insight
        UserInsight.objects.update_or_create(
            user=user,
            insight_type='journal_frequency',
            defaults={'data': data}
        )
        
        serializer = JournalAnalyticsSerializer(data)
        return Response(serializer.data)

class UserInsightsView(generics.ListAPIView):
    serializer_class = UserInsightSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return UserInsight.objects.none()
        return UserInsight.objects.filter(user=user)
