# backend/analytics/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Sum, Count, Q
from .models import UserProgress, TaskStats
from .serializers import UserProgressSerializer, TaskStatsSerializer
from accounts.models import CustomUser
from api.models import Course, Lesson, Progress

class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'teacher']:
            return UserProgress.objects.all()
        return UserProgress.objects.filter(user=user)


class TaskStatsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskStatsSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'teacher']:
            return TaskStats.objects.all()
        return TaskStats.objects.filter(user=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def analytics_dashboard(request):
    """Dashboard z analityką dla użytkownika"""
    user = request.user
    
    # Podstawowe statystyki
    completed = Progress.objects.filter(user=user, completed=True).count()
    total_score = Progress.objects.filter(user=user).aggregate(
        avg=Avg('score')
    )['avg'] or 0
    
    # Statystyki kursów
    courses_stats = []
    for course in Course.objects.filter(is_active=True):
        total_lessons = course.lessons.filter(is_active=True).count()
        completed_lessons = Progress.objects.filter(
            user=user,
            lesson__course=course,
            completed=True
        ).count()
        
        courses_stats.append({
            'course_id': course.id,
            'course_title': course.title,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percentage': round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0, 2)
        })
    
    # Aktywność w czasie
    from datetime import datetime, timedelta
    today = datetime.now().date()
    
    activity_last_7_days = []
    for i in range(7):
        date = today - timedelta(days=i)
        count = Progress.objects.filter(
            user=user,
            completed_at__date=date
        ).count()
        activity_last_7_days.append({
            'date': date.isoformat(),
            'lessons_completed': count
        })
    
    return Response({
        'user': {
            'id': str(user.id),
            'username': user.username,
            'points': user.points,
            'level': user.level
        },
        'stats': {
            'completed_lessons': completed,
            'average_score': round(total_score, 2),
            'total_points': user.points,
            'level': user.level
        },
        'courses': courses_stats,
        'activity': list(reversed(activity_last_7_days))
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommendations(request):
    """Rekomendacje kursów dla użytkownika"""
    user = request.user
    
    # Pobierz ukończone lekcje
    completed_lessons = Progress.objects.filter(
        user=user,
        completed=True
    ).values_list('lesson_id', flat=True)
    
    # Znajdź podobnych użytkowników (collaborative filtering)
    similar_users = CustomUser.objects.filter(
        role='student',
        level__range=(user.level - 1, user.level + 1)
    ).exclude(id=user.id)[:10]
    
    # Znajdź lekcje, które ukończyli podobni użytkownicy
    recommended_lessons = Lesson.objects.filter(
        progress__user__in=similar_users,
        progress__completed=True,
        is_active=True
    ).exclude(
        id__in=completed_lessons
    ).annotate(
        popularity=Count('progress')
    ).order_by('-popularity')[:10]
    
    recommendations_data = []
    for lesson in recommended_lessons:
        recommendations_data.append({
            'lesson_id': lesson.id,
            'lesson_title': lesson.title,
            'course_title': lesson.course.title,
            'difficulty': lesson.course.difficulty,
            'points': lesson.points,
            'duration_minutes': lesson.duration_minutes,
            'popularity_score': lesson.popularity
        })
    
    return Response({
        'recommendations': recommendations_data,
        'based_on': f'Poziom {user.level}, podobni użytkownicy'
    })

