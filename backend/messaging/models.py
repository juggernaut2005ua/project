from django.db import models
import uuid
from accounts.models import CustomUser

class Message(models.Model):
    MESSAGE_TYPES = [
        ('sync_request', 'Запрос синхронизации'),
        ('sync_response', 'Ответ синхронизации'),
        ('error', 'Ошибка'),
        ('notification', 'Уведомление'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPES)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    
    subject = models.CharField(max_length=255)
    body = models.TextField()
    payload = models.JSONField(default=dict, blank=True)
    
    is_read = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        indexes = [
            models.Index(fields=['to_user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.subject} ({self.get_message_type_display()})"

class Notification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('sent', 'Отправлено'),
        ('failed', 'Ошибка'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
