# backend/analytics/serializers.py
from rest_framework import serializers
from .models import UserProgress, TaskStats

class UserProgressSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = '__all__'


class TaskStatsSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    success_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = TaskStats
        fields = '__all__'
    
    def get_success_rate(self, obj):
        if obj.attempts == 0:
            return 0
        return round((obj.successes / obj.attempts) * 100, 2)