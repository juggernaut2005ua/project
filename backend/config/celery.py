# backend/config/celery.py
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('kodkids')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Scheduled tasks
app.conf.beat_schedule = {
    'sync-integration-tasks': {
        'task': 'integrations.tasks.run_scheduled_integrations',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'calculate-user-recommendations': {
        'task': 'analytics.tasks.calculate_all_recommendations',
        'schedule': crontab(hour='2', minute='0'),  # Daily at 2 AM
    },
    'cleanup-old-logs': {
        'task': 'analytics.tasks.cleanup_old_activity_logs',
        'schedule': crontab(day_of_month='1', hour='3', minute='0'),  # Monthly
    },
}