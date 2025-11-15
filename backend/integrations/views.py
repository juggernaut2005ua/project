# backend/integrations/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import SystemA, SystemB, IntegrationTask, IntegrationEvent, DataMapping
from .serializers import (
    SystemASerializer, SystemBSerializer, IntegrationTaskSerializer,
    IntegrationTaskCreateSerializer, IntegrationEventSerializer, DataMappingSerializer
)
from .tasks import run_integration_task

class SystemAViewSet(viewsets.ModelViewSet):
    queryset = SystemA.objects.all()
    serializer_class = SystemASerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test połączenia z systemem A"""
        system = self.get_object()
        from .utils import test_system_connection
        
        try:
            result = test_system_connection(system)
            return Response({
                'success': True,
                'message': 'Połączenie pomyślne',
                'details': result
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class SystemBViewSet(viewsets.ModelViewSet):
    queryset = SystemB.objects.all()
    serializer_class = SystemBSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def test_connection(self, request, pk=None):
        """Test połączenia z systemem B"""
        system = self.get_object()
        from .utils import test_system_connection
        
        try:
            result = test_system_connection(system)
            return Response({
                'success': True,
                'message': 'Połączenie pomyślne',
                'details': result
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class IntegrationTaskViewSet(viewsets.ModelViewSet):
    queryset = IntegrationTask.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return IntegrationTaskCreateSerializer
        return IntegrationTaskSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        """Uruchom zadanie integracji"""
        task = self.get_object()
        
        if task.status == 'running':
            return Response({
                'error': 'Zadanie jest już uruchomione'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Uruchom asynchronicznie przez Celery
        run_integration_task.delay(str(task.id))
        
        task.status = 'pending'
        task.save()
        
        return Response({
            'message': 'Zadanie zostało uruchomione',
            'task_id': str(task.id)
        })
    
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """Historia wydarzeń dla zadania"""
        task = self.get_object()
        events = task.events.all()
        
        page = self.paginate_queryset(events)
        if page is not None:
            serializer = IntegrationEventSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = IntegrationEventSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dashboard z statystykami integracji"""
        stats = {
            'total_tasks': IntegrationTask.objects.count(),
            'running_tasks': IntegrationTask.objects.filter(status='running').count(),
            'completed_tasks': IntegrationTask.objects.filter(status='completed').count(),
            'failed_tasks': IntegrationTask.objects.filter(status='failed').count(),
            'total_events': IntegrationEvent.objects.count(),
            'recent_errors': IntegrationEvent.objects.filter(
                event_type='error'
            ).order_by('-created_at')[:10]
        }
        
        stats['recent_errors'] = IntegrationEventSerializer(
            stats['recent_errors'], 
            many=True
        ).data
        
        return Response(stats)


class IntegrationEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = IntegrationEvent.objects.all()
    serializer_class = IntegrationEventSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['task', 'event_type']
    ordering_fields = ['created_at']
    search_fields = ['message']


class DataMappingViewSet(viewsets.ModelViewSet):
    queryset = DataMapping.objects.all()
    serializer_class = DataMappingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['task']
