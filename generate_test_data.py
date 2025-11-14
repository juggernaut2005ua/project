# backend/management/commands/generate_test_data.py
# Uruchomienie: python manage.py generate_test_data

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import *
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Generuje dane testowe dla platformy KodKids'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=50,
            help='Liczba użytkowników do wygenerowania'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        
        self.stdout.write('🚀 Rozpoczynam generowanie danych testowych...')
        
        # 1. Tworzenie kursów
        self.stdout.write('📚 Tworzenie kursów...')
        courses = self.create_courses()
        
        # 2. Tworzenie lekcji
        self.stdout.write('📝 Tworzenie lekcji...')
        lessons = self.create_lessons(courses)
        
        # 3. Tworzenie ćwiczeń
        self.stdout.write('✏️ Tworzenie ćwiczeń...')
        self.create_exercises(lessons)
        
        # 4. Tworzenie osiągnięć
        self.stdout.write('🏆 Tworzenie osiągnięć...')
        achievements = self.create_achievements()
        
        # 5. Tworzenie użytkowników
        self.stdout.write(f'👥 Tworzenie {num_users} użytkowników...')
        users = self.create_users(num_users)
        
        # 6. Generowanie postępów
        self.stdout.write('📊 Generowanie postępów...')
        self.create_progress(users, lessons)
        
        # 7. Przyznawanie osiągnięć
        self.stdout.write('🎖️ Przyznawanie osiągnięć...')
        self.assign_achievements(users, achievements)
        
        # 8. Generowanie logów aktywności
        self.stdout.write('📋 Generowanie logów aktywności...')
        self.create_activity_logs(users, lessons)
        
        self.stdout.write(self.style.SUCCESS('✅ Dane testowe wygenerowane pomyślnie!'))
        self.stdout.write(f'   - Kursy: {len(courses)}')
        self.stdout.write(f'   - Lekcje: {len(lessons)}')
        self.stdout.write(f'   - Użytkownicy: {len(users)}')
        self.stdout.write(f'   - Osiągnięcia: {len(achievements)}')

    def create_courses(self):
        courses_data = [
            {
                'title': 'Podstawy Scratch',
                'description': 'Naucz się tworzyć gry i animacje w prostym języku wizualnym',
                'difficulty': 'beginner',
                'icon': 'code',
                'color': 'blue',
                'order': 1
            },
            {
                'title': 'Python dla Dzieci',
                'description': 'Pierwsze kroki w programowaniu tekstowym z Pythonem',
                'difficulty': 'beginner',
                'icon': 'zap',
                'color': 'yellow',
                'order': 2
            },
            {
                'title': 'HTML & CSS',
                'description': 'Twórz własne strony internetowe od podstaw',
                'difficulty': 'intermediate',
                'icon': 'star',
                'color': 'purple',
                'order': 3
            },
            {
                'title': 'JavaScript dla Młodych',
                'description': 'Dodaj interaktywność do swoich stron internetowych',
                'difficulty': 'intermediate',
                'icon': 'trophy',
                'color': 'green',
                'order': 4
            },
            {
                'title': 'Aplikacje Mobilne',
                'description': 'Twórz aplikacje na telefony i tablety',
                'difficulty': 'advanced',
                'icon': 'target',
                'color': 'red',
                'order': 5
            },
            {
                'title': 'Gry 2D',
                'description': 'Stwórz własną grę komputerową od zera',
                'difficulty': 'advanced',
                'icon': 'gamepad',
                'color': 'orange',
                'order': 6
            }
        ]
        
        courses = []
        for data in courses_data:
            course, created = Course.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            courses.append(course)
            if created:
                self.stdout.write(f'  ✓ Utworzono kurs: {course.title}')
        
        return courses

    def create_lessons(self, courses):
        lessons_templates = {
            'Podstawy Scratch': [
                ('Witaj w Scratch!', 'Poznaj interfejs i podstawowe bloki', 10, 15),
                ('Pierwszy projekt', 'Stwórz swoją pierwszą animację', 15, 20),
                ('Duszki i kostiumy', 'Naucz się dodawać i animować postaci', 15, 25),
                ('Ruch i animacja', 'Sprawdź jak poruszać duszkami', 20, 30),
                ('Dźwięki', 'Dodaj muzykę i efekty dźwiękowe', 15, 20),
                ('Zmienne', 'Przechowuj informacje w zmiennych', 20, 35),
                ('Warunki', 'Podejmuj decyzje w kodzie', 25, 40),
                ('Pętle', 'Powtarzaj działania automatycznie', 25, 40),
                ('Klonowanie', 'Twórz kopie duszków', 20, 35),
                ('Moja pierwsza gra', 'Stwórz prostą grę zręcznościową', 30, 60),
            ],
            'Python dla Dzieci': [
                ('Co to jest Python?', 'Wprowadzenie do języka Python', 10, 15),
                ('Instalacja i pierwsze kroki', 'Uruchom swój pierwszy program', 15, 25),
                ('Zmienne i typy danych', 'Przechowuj różne rodzaje informacji', 20, 30),
                ('Operatory matematyczne', 'Liczenie w Pythonie', 15, 25),
                ('Teksty (stringi)', 'Praca z tekstem', 20, 30),
                ('Wprowadzanie danych', 'Komunikacja z użytkownikiem', 15, 25),
                ('Instrukcje warunkowe', 'if, elif, else', 25, 35),
                ('Pętle for', 'Powtarzanie z pętlą for', 25, 35),
                ('Pętle while', 'Powtarzanie z pętlą while', 25, 35),
                ('Listy', 'Przechowywanie wielu wartości', 30, 40),
                ('Funkcje', 'Twórz własne funkcje', 30, 45),
                ('Projekt końcowy', 'Aplikacja konsolowa', 40, 60),
            ],
            'HTML & CSS': [
                ('Czym jest HTML?', 'Wprowadzenie do budowy stron', 10, 15),
                ('Struktura dokumentu', 'Podstawowe tagi HTML', 15, 20),
                ('Tekst i formatowanie', 'Nagłówki, akapity, listy', 20, 25),
                ('Linki i obrazy', 'Dodawanie odnośników i grafik', 20, 30),
                ('Wprowadzenie do CSS', 'Stylowanie elementów', 20, 30),
                ('Kolory i czcionki', 'Personalizacja wyglądu', 25, 35),
                ('Box Model', 'Marginesy, paddingi, obramowania', 25, 40),
                ('Layout', 'Rozmieszczenie elementów', 30, 45),
                ('Responsywność', 'Strona na różnych urządzeniach', 30, 45),
                ('Twoja pierwsza strona', 'Projekt kompletnej strony', 45, 90),
            ]
        }
        
        all_lessons = []
        for course in courses:
            if course.title in lessons_templates:
                templates = lessons_templates[course.title]
                for idx, (title, content, points, duration) in enumerate(templates, 1):
                    lesson, created = Lesson.objects.get_or_create(
                        course=course,
                        title=title,
                        defaults={
                            'content': content,
                            'order': idx,
                            'points': points,
                            'duration_minutes': duration
                        }
                    )
                    all_lessons.append(lesson)
        
        return all_lessons

    def create_exercises(self, lessons):
        exercise_types = ['quiz', 'code', 'drag_drop']
        
        for lesson in lessons[:30]:  # Dla pierwszych 30 lekcji
            num_exercises = random.randint(2, 5)
            for i in range(num_exercises):
                exercise_type = random.choice(exercise_types)
                
                content = self.generate_exercise_content(exercise_type, lesson)
                
                Exercise.objects.get_or_create(
                    lesson=lesson,
                    title=f'Ćwiczenie {i+1}: {lesson.title}',
                    defaults={
                        'description': f'Sprawdź swoją wiedzę z lekcji: {lesson.title}',
                        'exercise_type': exercise_type,
                        'content': content,
                        'points': random.randint(5, 15),
                        'order': i + 1
                    }
                )

    def generate_exercise_content(self, exercise_type, lesson):
        if exercise_type == 'quiz':
            return {
                'question': f'Pytanie testowe z lekcji {lesson.title}',
                'options': ['Opcja A', 'Opcja B', 'Opcja C', 'Opcja D'],
                'correct_answer': 'Opcja A'
            }
        elif exercise_type == 'code':
            return {
                'instructions': 'Napisz kod rozwiązujący problem',
                'starter_code': 'def solution():\n    pass',
                'test_cases': [
                    {'input': '1', 'output': '1'},
                    {'input': '2', 'output': '4'}
                ]
            }
        else:  # drag_drop
            return {
                'items': ['Element 1', 'Element 2', 'Element 3'],
                'correct_order': [0, 1, 2]
            }

    def create_achievements(self):
        achievements_data = [
            ('Początkujący', 'Ukończ pierwszą lekcję', 'star', 0),
            ('Bystry uczeń', 'Zdobądź 100 punktów', 'award', 100),
            ('Programista', 'Ukończ 10 lekcji', 'code', 0),
            ('Expert', 'Zdobądź 500 punktów', 'trophy', 500),
            ('Mistrz', 'Ukończ cały kurs', 'crown', 0),
            ('Wytrwały', 'Loguj się 7 dni z rzędu', 'calendar', 0),
            ('Szybki', 'Ukończ lekcję w mniej niż 10 minut', 'zap', 0),
            ('Perfekcjonista', 'Zdobądź 100% w 5 lekcjach', 'target', 0),
            ('Społeczny', 'Pomóż 5 innym uczniom', 'users', 0),
            ('Legenda', 'Zdobądź 1000 punktów', 'medal', 1000),
        ]
        
        achievements = []
        for name, description, icon, points_req in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'icon': icon,
                    'points_required': points_req
                }
            )
            achievements.append(achievement)
        
        return achievements

    def create_users(self, num_users):
        users = []
        
        # Admin
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@kodkids.pl',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'points': 0,
                'level': 1
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
        
        # Nauczyciele
        for i in range(3):
            teacher, created = User.objects.get_or_create(
                username=f'teacher{i+1}',
                defaults={
                    'email': f'teacher{i+1}@kodkids.pl',
                    'role': 'teacher',
                    'age': random.randint(25, 50),
                    'points': 0,
                    'level': 1
                }
            )
            if created:
                teacher.set_password('teacher123')
                teacher.save()
        
        # Uczniowie
        first_names = ['Adam', 'Ewa', 'Jan', 'Anna', 'Piotr', 'Maria', 'Tomasz', 'Zofia', 
                       'Michał', 'Maja', 'Jakub', 'Julia', 'Kacper', 'Zuzanna', 'Filip']
        
        for i in range(num_users):
            name = random.choice(first_names)
            username = f'{name.lower()}{random.randint(100, 999)}'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'role': 'student',
                    'age': random.randint(7, 16),
                    'points': random.randint(0, 500),
                    'level': random.randint(1, 5)
                }
            )
            if created:
                user.set_password('student123')
                user.save()
                users.append(user)
        
        return users

    def create_progress(self, users, lessons):
        for user in users:
            # Każdy użytkownik ukończył losową liczbę lekcji
            num_completed = random.randint(0, min(15, len(lessons)))
            completed_lessons = random.sample(lessons, num_completed)
            
            for lesson in completed_lessons:
                score = random.randint(70, 100)
                attempts = random.randint(1, 3)
                
                Progress.objects.get_or_create(
                    user=user,
                    lesson=lesson,
                    defaults={
                        'completed': True,
                        'score': score,
                        'attempts': attempts,
                        'completed_at': datetime.now() - timedelta(
                            days=random.randint(0, 30)
                        )
                    }
                )

    def assign_achievements(self, users, achievements):
        for user in users:
            # Przyznaj losowe osiągnięcia w zależności od punktów
            eligible = [a for a in achievements if a.points_required <= user.points]
            num_achievements = random.randint(0, len(eligible))
            
            for achievement in random.sample(eligible, num_achievements):
                UserAchievement.objects.get_or_create(
                    user=user,
                    achievement=achievement,
                    defaults={
                        'earned_at': datetime.now() - timedelta(
                            days=random.randint(0, 30)
                        )
                    }
                )

    def create_activity_logs(self, users, lessons):
        actions = ['login', 'lesson_complete', 'exercise_complete']
        
        for user in users:
            num_logs = random.randint(5, 30)
            for _ in range(num_logs):
                action = random.choice(actions)
                details = {}
                
                if action == 'lesson_complete':
                    details = {
                        'lesson_id': random.choice(lessons).id,
                        'score': random.randint(70, 100)
                    }
                
                ActivityLog.objects.create(
                    user=user,
                    action=action,
                    details=details,
                    ip_address=f'192.168.1.{random.randint(1, 255)}',
                    created_at=datetime.now() - timedelta(
                        days=random.randint(0, 30),
                        hours=random.randint(0, 23)
                    )
                )


# Fixture JSON dla szybkiego załadowania danych
# backend/fixtures/initial_data.json
"""
[
  {
    "model": "api.course",
    "pk": 1,
    "fields": {
      "title": "Podstawy Scratch",
      "description": "Naucz się tworzyć gry i animacje",
      "difficulty": "beginner",
      "icon": "code",
      "color": "blue",
      "order": 1,
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  }
]
"""

# Makefile dla łatwego zarządzania
"""
# Makefile

.PHONY: install migrate test run clean docker-up docker-down

install:
\tpip install -r requirements.txt
\tcd frontend && npm install

migrate:
\tpython manage.py makemigrations
\tpython manage.py migrate

test-data:
\tpython manage.py generate_test_data --users 50

superuser:
\tpython manage.py createsuperuser

test:
\tpytest
\tcd frontend && npm test

run-backend:
\tpython manage.py runserver

run-frontend:
\tcd frontend && npm start

run-celery:
\tcelery -A config worker -l info

docker-up:
\tdocker-compose up -d

docker-down:
\tdocker-compose down

docker-logs:
\tdocker-compose logs -f

docker-shell:
\tdocker-compose exec backend python manage.py shell

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {} +
\tfind . -type f -name "*.pyc" -delete
\trm -rf .pytest_cache
\trm -rf htmlcov
\trm -rf .coverage
"""