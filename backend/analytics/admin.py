# backend/analytics/admin.py
from django.contrib import admin
from .models import UserProgress, TaskStats

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'tasks_completed', 'points_earned', 'level', 'updated_at']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(TaskStats)
class TaskStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'task_name', 'attempts', 'successes', 'avg_time', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'task_name']
    readonly_fields = ['id', 'created_at', 'updated_at']