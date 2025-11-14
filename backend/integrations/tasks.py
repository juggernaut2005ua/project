from celery import shared_task
from django.utils import timezone
import time
from .models import IntegrationTask, IntegrationEvent
from .utils import sync_data_between_systems

@shared_task
def run_integration_task(task_id):
    """Запускает асинхронную задачу интеграции"""
    try:
        task = IntegrationTask.objects.get(id=task_id)
        task.status = 'running'
        task.save()
        
        start_time = time.time()
        
        # Синхронизируем данные
        result = sync_data_between_systems(task)
        
        sync_duration = time.time() - start_time
        
        # Создаем событие
        IntegrationEvent.objects.create(
            task=task,
            event_type='sync_complete',
            message='Синхронизация успешно завершена',
            records_synced=result.get('records_synced', 0),
            sync_duration=sync_duration,
        )
        
        task.status = 'completed'
        task.last_run = timezone.now()
        task.save()
        
        return {'status': 'completed', 'records_synced': result.get('records_synced', 0)}
    
    except Exception as e:
        IntegrationEvent.objects.create(
            task=task,
            event_type='error',
            message='Ошибка при синхронизации',
            error_details={'error': str(e)},
        )
        task.status = 'failed'
        task.save()
        raise
