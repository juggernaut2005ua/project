from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemAViewSet, SystemBViewSet, IntegrationTaskViewSet,
    IntegrationEventViewSet, DataMappingViewSet
)

router = DefaultRouter()
router.register(r'system-a', SystemAViewSet, basename='system-a')
router.register(r'system-b', SystemBViewSet, basename='system-b')
router.register(r'tasks', IntegrationTaskViewSet, basename='integration-task')
router.register(r'events', IntegrationEventViewSet, basename='integration-event')
router.register(r'mappings', DataMappingViewSet, basename='data-mapping')

urlpatterns = [
    path('', include(router.urls)),
]
