from django.db import models
import uuid
from accounts.models import CustomUser

class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='progress')
    
    tasks_completed = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
    
    def __str__(self):
        return f"{self.user.username} - Уровень {self.level}"

class TaskStats(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='task_stats')
    
    task_name = models.CharField(max_length=255)
    attempts = models.IntegerField(default=0)
    successes = models.IntegerField(default=0)
    avg_time = models.FloatField(help_text='Среднее время выполнения в секундах', default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Статистика задачи'
        verbose_name_plural = 'Статистики задач'
        unique_together = ('user', 'task_name')
    
    def __str__(self):
        return f"{self.user.username} - {self.task_name}"
