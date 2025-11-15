# backend/accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Uczeń'),
        ('teacher', 'Nauczyciel'),
        ('parent', 'Rodzic'),
        ('admin', 'Administrator'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    age = models.IntegerField(
        null=True, 
        blank=True, 
        validators=[MinValueValidator(5), MaxValueValidator(18)]
    )
    points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    two_factor_enabled = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    parent_email = models.EmailField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Użytkownik'
        verbose_name_plural = 'Użytkownicy'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def add_points(self, points):
        """Dodaje punkty i sprawdza awans poziomu"""
        self.points += points
        new_level = (self.points // 100) + 1
        if new_level > self.level:
            self.level = new_level
        self.save()
        return self.level

