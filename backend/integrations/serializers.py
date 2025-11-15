# backend/integrations/serializers.py
from rest_framework import serializers
from .models import SystemA, SystemB, IntegrationTask, IntegrationEvent, DataMapping

class SystemASerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemA
        fields = '__all__'
        extra_kwargs = {
            'api_key': {'write_only': True}
        }


class SystemBSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemB
        fields = '__all__'
        extra_kwargs = {
            'api_key': {'write_only': True}
        }


class DataMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMapping
        fields = '__all__'


class IntegrationEventSerializer(serializers.ModelSerializer):
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    
    class Meta:
        model = IntegrationEvent
        fields = '__all__'


class IntegrationTaskSerializer(serializers.ModelSerializer):
    system_a_name = serializers.CharField(source='system_a.name', read_only=True)
    system_b_name = serializers.CharField(source='system_b.name', read_only=True)
    direction_display = serializers.CharField(source='get_direction_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    mappings = DataMappingSerializer(many=True, read_only=True)
    recent_events = serializers.SerializerMethodField()
    
    class Meta:
        model = IntegrationTask
        fields = '__all__'
    
    def get_recent_events(self, obj):
        events = obj.events.all()[:5]
        return IntegrationEventSerializer(events, many=True).data


class IntegrationTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationTask
        fields = [
            'name', 'description', 'system_a', 'system_b', 
            'direction', 'schedule_enabled', 'schedule_interval'
        ]