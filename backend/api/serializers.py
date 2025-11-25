from rest_framework import serializers
from .models import Course, Lesson, Progress, UserAchievement


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_active', 'difficulty']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'points', 'duration_minutes', 'is_active']


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = ['id', 'user', 'lesson', 'completed', 'completed_at', 'score']


class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ['id', 'user', 'name', 'awarded_at']
