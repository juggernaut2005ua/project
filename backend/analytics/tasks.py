# backend/analytics/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def calculate_all_recommendations():
    """Oblicza rekomendacje dla wszystkich użytkowników"""
    from accounts.models import CustomUser
    
    users = CustomUser.objects.filter(role='student', is_active=True)
    
    for user in users:
        try:
            calculate_user_recommendations(user)
        except Exception as e:
            logger.error(f"Błąd przy obliczaniu rekomendacji dla {user.username}: {e}")
    
    logger.info(f"Obliczono rekomendacje dla {users.count()} użytkowników")


def calculate_user_recommendations(user):
    """Oblicza rekomendacje dla pojedynczego użytkownika"""
    # Logika rekomendacji - można rozbudować o ML
    pass


@shared_task
def cleanup_old_activity_logs():
    """Usuwa stare logi aktywności"""
    from api.models import ActivityLog
    
    cutoff_date = timezone.now() - timedelta(days=90)
    deleted_count = ActivityLog.objects.filter(created_at__lt=cutoff_date).delete()[0]
    
    logger.info(f"Usunięto {deleted_count} starych logów aktywności")
    return deleted_count