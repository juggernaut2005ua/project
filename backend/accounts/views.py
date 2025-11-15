# backend/accounts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, 
    UserSerializer, 
    UserProfileSerializer
)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Rejestracja nowego użytkownika"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Rejestracja pomyślna',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Logowanie użytkownika"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })
    
    return Response(
        {'error': 'Nieprawidłowe dane logowania'}, 
        status=status.HTTP_401_UNAUTHORIZED
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return CustomUser.objects.all()
        elif user.role == 'teacher':
            return CustomUser.objects.filter(role='student')
        else:
            return CustomUser.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Dane zalogowanego użytkownika"""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'])
    def update_profile(self, request):
        """Aktualizacja profilu"""
        serializer = UserProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statystyki użytkownika"""
        user = request.user
        
        from api.models import Progress, UserAchievement
        
        stats = {
            'total_points': user.points,
            'level': user.level,
            'completed_lessons': Progress.objects.filter(
                user=user, 
                completed=True
            ).count(),
            'achievements': UserAchievement.objects.filter(user=user).count(),
            'avg_score': Progress.objects.filter(user=user).aggregate(
                models.Avg('score')
            )['score__avg'] or 0,
        }
        
        return Response(stats)