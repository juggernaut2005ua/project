# backend/analytics/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProgressViewSet, 
    TaskStatsViewSet,
    analytics_dashboard,
    recommendations
)

router = DefaultRouter()
router.register('progress', UserProgressViewSet, basename='user-progress')
router.register('task-stats', TaskStatsViewSet, basename='task-stats')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', analytics_dashboard, name='analytics-dashboard'),
    path('recommendations/', recommendations, name='recommendations'),
]

