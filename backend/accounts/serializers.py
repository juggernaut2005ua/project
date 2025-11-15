# backend/accounts/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'role', 'age', 'parent_email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Hasła nie są identyczne"})
        
        if attrs['role'] == 'student' and not attrs.get('parent_email'):
            raise serializers.ValidationError({"parent_email": "Email rodzica jest wymagany dla uczniów"})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'role', 'age', 'points', 
            'level', 'avatar', 'parent_email', 'created_at'
        ]
        read_only_fields = ['id', 'points', 'level', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'role', 'age', 'points', 'level', 'avatar', 
            'parent_email', 'two_factor_enabled', 'created_at'
        ]
        read_only_fields = ['id', 'points', 'level', 'created_at', 'role']
