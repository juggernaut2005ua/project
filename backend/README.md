# backend/README.md
# KodKids Platform - Backend

## Opis projektu
Backend platformy edukacyjnej dla dzieci do nauki programowania.

## Technologie
- Django 4.2
- Django REST Framework
- PostgreSQL
- Redis
- RabbitMQ
- Celery

## Instalacja

### Wymagania
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- RabbitMQ 3.12+

### Krok po kroku

1. Klonuj repozytorium i przejdź do katalogu backend
```bash
cd backend
```

2. Utwórz wirtualne środowisko
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate  # Windows
```

3. Zainstaluj zależności
```bash
pip install -r requirements.txt
```

4. Skopiuj plik .env.example i dostosuj konfigurację
```bash
cp .env.example .env
```

5. Wykonaj migracje
```bash
python manage.py migrate
```

6. Utwórz superusera
```bash
python manage.py createsuperuser
```

7. Załaduj dane testowe (opcjonalnie)
```bash
python manage.py generate_test_data --users 50
```

8. Uruchom serwer
```bash
python manage.py runserver
```

## API Endpoints

### Autentykacja
- POST `/api/auth/register/` - Rejestracja
- POST `/api/auth/login/` - Logowanie (JWT)
- POST `/api/auth/refresh/` - Odświeżenie tokenu
- POST `/api/auth/logout/` - Wylogowanie

### Kursy
- GET `/api/courses/` - Lista kursów
- GET `/api/courses/{id}/` - Szczegóły kursu
- GET `/api/courses/{id}/lessons/` - Lekcje kursu

### Lekcje
- GET `/api/lessons/` - Lista lekcji
- GET `/api/lessons/{id}/` - Szczegóły lekcji
- POST `/api/lessons/{id}/complete/` - Ukończenie lekcji

### Użytkownicy
- GET `/api/users/me/` - Dane użytkownika
- GET `/api/users/stats/` - Statystyki użytkownika

### Dokumentacja API
- Swagger UI: http://localhost:8000/api/docs/
- Schema: http://localhost:8000/api/schema/

## Testy
```bash
pytest
pytest --cov
```

## Celery Workers
```bash
# Worker
celery -A config worker -l info

# Beat (scheduler)
celery -A config beat -l info
```

## Struktura projektu
```
backend/
├── accounts/          # Moduł użytkowników
├── api/              # Główne API (kursy, lekcje)
├── integrations/     # Moduł integracji systemów
├── analytics/        # Moduł analiz i statystyk
├── messaging/        # Moduł wiadomości
├── config/           # Konfiguracja Django
├── static/           # Pliki statyczne
├── media/            # Pliki użytkowników
└── logs/             # Logi aplikacji
```