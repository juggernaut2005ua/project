from django.db import models
import uuid
from accounts.models import CustomUser

class SystemA(models.Model):
    """Модель для первой интегрируемой системы (например, CRM)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    api_endpoint = models.URLField()
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Система A (CRM)'
        verbose_name_plural = 'Системы A (CRM)'
    
    def __str__(self):
        return self.name


class SystemB(models.Model):
    """Модель для второй интегрируемой системы (например, система управления запасами)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    api_endpoint = models.URLField()
    api_key = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Система B (Управление запасами)'
        verbose_name_plural = 'Системы B (Управление запасами)'
    
    def __str__(self):
        return self.name


class IntegrationTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('running', 'В процессе'),
        ('completed', 'Завершена'),
        ('failed', 'Ошибка'),
    ]
    
    DIRECTION_CHOICES = [
        ('a_to_b', 'A → B'),
        ('b_to_a', 'B → A'),
        ('bidirectional', 'Двусторонняя'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    system_a = models.ForeignKey(SystemA, on_delete=models.CASCADE)
    system_b = models.ForeignKey(SystemB, on_delete=models.CASCADE)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    
    # Конфигурация
    schedule_enabled = models.BooleanField(default=False)
    schedule_interval = models.IntegerField(help_text='Интервал в минутах', null=True, blank=True)
    
    # Логирование
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_run = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Задача интеграции'
        verbose_name_plural = 'Задачи интеграции'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_direction_display()})"


class IntegrationEvent(models.Model):
    EVENT_TYPES = [
        ('sync_start', 'Начало синхронизации'),
        ('sync_complete', 'Синхронизация завершена'),
        ('error', 'Ошибка'),
        ('data_mismatch', 'Несоответствие данных'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(IntegrationTask, on_delete=models.CASCADE, related_name='events')
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    message = models.TextField()
    error_details = models.JSONField(null=True, blank=True)
    
    # Синхронизированные данные
    records_synced = models.IntegerField(default=0)
    sync_duration = models.FloatField(help_text='Длительность в секундах', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Событие интеграции'
        verbose_name_plural = 'События интеграции'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['task', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_event_type_display()} - {self.task.name}"


class DataMapping(models.Model):
    """Маппинг полей между двумя системами"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(IntegrationTask, on_delete=models.CASCADE, related_name='mappings')
    
    field_a = models.CharField(max_length=255, help_text='Поле из системы A')
    field_b = models.CharField(max_length=255, help_text='Поле из системы B')
    
    transformation_rule = models.TextField(blank=True, help_text='Правило трансформации (JSON)')
    is_required = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Маппинг данных'
        verbose_name_plural = 'Маппинги данных'
        unique_together = ('task', 'field_a', 'field_b')
    
    def __str__(self):
        return f"{self.field_a} → {self.field_b}"
