# backend/integrations/tasks.py - ROZSZERZONE
from celery import shared_task
from django.utils import timezone
import time
from .models import IntegrationTask, IntegrationEvent
from .utils import sync_data_between_systems
import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def run_integration_task(self, task_id):
    """Uruchamia zadanie integracji"""
    try:
        task = IntegrationTask.objects.get(id=task_id)
        task.status = 'running'
        task.save()
        
        logger.info(f"Uruchamiam zadanie integracji: {task.name}")
        
        IntegrationEvent.objects.create(
            task=task,
            event_type='sync_start',
            message='Rozpoczęto synchronizację danych'
        )
        
        start_time = time.time()
        
        # Synchronizuj dane
        result = sync_data_between_systems(task)
        
        sync_duration = time.time() - start_time
        
        # Zapisz wydarzenie sukcesu
        IntegrationEvent.objects.create(
            task=task,
            event_type='sync_complete',
            message='Synchronizacja zakończona pomyślnie',
            records_synced=result.get('records_synced', 0),
            sync_duration=sync_duration
        )
        
        task.status = 'completed'
        task.last_run = timezone.now()
        task.save()
        
        logger.info(f"Zadanie {task.name} zakończone pomyślnie")
        
        return {
            'status': 'completed',
            'records_synced': result.get('records_synced', 0),
            'duration': sync_duration
        }
    
    except Exception as e:
        logger.error(f"Błąd w zadaniu integracji: {str(e)}")
        
        IntegrationEvent.objects.create(
            task=task,
            event_type='error',
            message=f'Błąd podczas synchronizacji: {str(e)}',
            error_details={'error': str(e), 'traceback': str(e.__traceback__)}
        )
        
        task.status = 'failed'
        task.save()
        
        # Retry jeśli to możliwe
        if self.request.retries < self.max_retries:
            raise self.retry(exc=e, countdown=60 * (self.request.retries + 1))
        
        raise


@shared_task
def run_scheduled_integrations():
    """Uruchamia zaplanowane zadania integracji"""
    tasks = IntegrationTask.objects.filter(
        schedule_enabled=True,
        status__in=['pending', 'completed', 'failed']
    )
    
    for task in tasks:
        logger.info(f"Uruchamiam zaplanowane zadanie: {task.name}")
        run_integration_task.delay(str(task.id))