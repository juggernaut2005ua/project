# Instrukcja Instalacji Platformy KodKids

## Wymagania Systemowe

### Minimalne wymagania
- **OS**: Linux (Ubuntu 20.04+), macOS 11+, Windows 10+ (z WSL2)
- **RAM**: 8 GB
- **Procesor**: 4 rdzenie
- **Dysk**: 20 GB wolnej przestrzeni

### Oprogramowanie
- Python 3.10+
- Node.js 18+ i npm
- PostgreSQL 15+
- Redis 7+
- RabbitMQ 3.12+
- Docker & Docker Compose (opcjonalnie)

## Instalacja - Metoda 1: Docker (Zalecana)

### Krok 1: Przygotowanie środowiska

```bash
# Klonowanie repozytorium
git clone https://github.com/your-org/kodkids-platform.git
cd kodkids-platform

# Utworzenie plików konfiguracyjnych
cp .env.example .env
```

### Krok 2: Konfiguracja .env

```bash
# Backend Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=kids_coding_platform
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0

# RabbitMQ
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
```

### Krok 3: Uruchomienie z Docker Compose

```bash
# Zbudowanie i uruchomienie wszystkich kontenerów
docker-compose up -d --build

# Sprawdzenie statusu
docker-compose ps

# Logi
docker-compose logs -f
```

### Krok 4: Migracje i dane początkowe

```bash
# Wykonanie migracji bazy danych
docker-compose exec backend python manage.py migrate

# Utworzenie superusera
docker-compose exec backend python manage.py createsuperuser

# Załadowanie przykładowych danych
docker-compose exec backend python manage.py loaddata fixtures/initial_data.json
```

### Krok 5: Dostęp do aplikacji

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **RabbitMQ Management**: http://localhost:15672 (guest/guest)

---

## Instalacja - Metoda 2: Manualna

### Krok 1: Instalacja PostgreSQL

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Utworzenie bazy danych
sudo -u postgres psql
CREATE DATABASE kids_coding_platform;
CREATE USER kodkids WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE kids_coding_platform TO kodkids;
\q
```

#### macOS (Homebrew)
```bash
brew install postgresql@15
brew services start postgresql@15

createdb kids_coding_platform
```

#### Windows
1. Pobierz instalator z https://www.postgresql.org/download/windows/
2. Uruchom instalator i postępuj zgodnie z instrukcjami
3. Użyj pgAdmin do utworzenia bazy danych

### Krok 2: Instalacja Redis

#### Ubuntu/Debian
```bash
sudo apt install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Test połączenia
redis-cli ping
# Powinno zwrócić: PONG
```

#### macOS
```bash
brew install redis
brew services start redis
```

#### Windows
Pobierz z: https://github.com/microsoftarchive/redis/releases

### Krok 3: Instalacja RabbitMQ

#### Ubuntu/Debian
```bash
sudo apt install rabbitmq-server
sudo systemctl start rabbitmq-server
sudo systemctl enable rabbitmq-server

# Włączenie panelu zarządzania
sudo rabbitmq-plugins enable rabbitmq_management

# Utworzenie użytkownika
sudo rabbitmqctl add_user admin admin123
sudo rabbitmqctl set_user_tags admin administrator
sudo rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"
```

#### macOS
```bash
brew install rabbitmq
brew services start rabbitmq
rabbitmq-plugins enable rabbitmq_management
```

### Krok 4: Backend (Django)

```bash
# Przejście do katalogu backend
cd backend

# Utworzenie środowiska wirtualnego
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# lub
venv\Scripts\activate  # Windows

# Instalacja zależności
pip install -r requirements.txt

# Konfiguracja zmiennych środowiskowych
export SECRET_KEY='your-secret-key'
export DB_NAME='kids_coding_platform'
export DB_USER='kodkids'
export DB_PASSWORD='secure_password'
export DB_HOST='localhost'
export DB_PORT='5432'

# Migracje
python manage.py makemigrations
python manage.py migrate

# Utworzenie superusera
python manage.py createsuperuser

# Załadowanie danych początkowych
python manage.py loaddata fixtures/courses.json
python manage.py loaddata fixtures/achievements.json

# Uruchomienie serwera deweloperskiego
python manage.py runserver 0.0.0.0:8000
```

### Krok 5: Celery Workers

Otwórz nowy terminal:

```bash
cd backend
source venv/bin/activate

# Uruchomienie Celery worker
celery -A config worker -l info

# W kolejnym terminalu: Celery Beat (scheduler)
celery -A config beat -l info
```

### Krok 6: Frontend (React)

```bash
# Przejście do katalogu frontend
cd frontend

# Instalacja zależności
npm install

# Konfiguracja
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env

# Uruchomienie serwera deweloperskiego
npm start

# Aplikacja będzie dostępna na http://localhost:3000
```

---

## Konfiguracja Produkcyjna

### 1. Bezpieczeństwo

#### Generowanie bezpiecznych kluczy
```bash
# Django SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# JWT Secret
openssl rand -base64 32
```

#### SSL/TLS (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d kodkids.pl -d www.kodkids.pl
```

### 2. Nginx Configuration

```nginx
# /etc/nginx/sites-available/kodkids

upstream backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name kodkids.pl www.kodkids.pl;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name kodkids.pl www.kodkids.pl;

    ssl_certificate /etc/letsencrypt/live/kodkids.pl/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kodkids.pl/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;

    # Frontend
    location / {
        root /var/www/kodkids/frontend/build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/kodkids/backend/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /var/www/kodkids/backend/media/;
    }
}
```

```bash
# Aktywacja konfiguracji
sudo ln -s /etc/nginx/sites-available/kodkids /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 3. Gunicorn (WSGI Server)

```bash
# Instalacja
pip install gunicorn

# Konfiguracja
# gunicorn_config.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "info"

# Uruchomienie
gunicorn config.wsgi:application -c gunicorn_config.py
```

### 4. Systemd Service

```ini
# /etc/systemd/system/kodkids-backend.service

[Unit]
Description=KodKids Django Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/kodkids/backend
Environment="PATH=/var/www/kodkids/backend/venv/bin"
ExecStart=/var/www/kodkids/backend/venv/bin/gunicorn \
    --config gunicorn_config.py \
    config.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Aktywacja
sudo systemctl daemon-reload
sudo systemctl start kodkids-backend
sudo systemctl enable kodkids-backend
sudo systemctl status kodkids-backend
```

### 5. Celery Systemd Services

```ini
# /etc/systemd/system/celery-worker.service

[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/var/www/kodkids/backend
ExecStart=/var/www/kodkids/backend/venv/bin/celery multi start worker \
    -A config --pidfile=/var/run/celery/%n.pid \
    --logfile=/var/log/celery/%n%I.log --loglevel=INFO

[Install]
WantedBy=multi-user.target
```

---

## Testowanie Instalacji

### 1. Backend API Tests

```bash
cd backend
python manage.py test

# Z pokryciem kodu
coverage run --source='.' manage.py test
coverage report
coverage html
```

### 2. Frontend Tests

```bash
cd frontend
npm test

# E2E tests (jeśli zaimplementowane)
npm run test:e2e
```

### 3. Integration Tests

```bash
# Test połączenia z bazą danych
python manage.py dbshell

# Test Redis
redis-cli ping

# Test RabbitMQ
curl -u guest:guest http://localhost:15672/api/overview
```

### 4. Load Testing

```bash
# Instalacja Locust
pip install locust

# Uruchomienie testów obciążeniowych
locust -f tests/load_test.py --host=http://localhost:8000
```

---

## Monitoring i Logowanie

### 1. Logowanie

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/kodkids/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### 2. Prometheus Metrics

```bash
# Instalacja
pip install django-prometheus

# settings.py
INSTALLED_APPS = [
    'django_prometheus',
    ...
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    ...
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]
```

### 3. Grafana Dashboard

Import gotowych dashboardów:
- Django Metrics
- PostgreSQL Database
- Redis Monitoring
- RabbitMQ Overview

---

## Backup i Restore

### Database Backup

```bash
# Backup
pg_dump -U kodkids kids_coding_platform > backup_$(date +%Y%m%d).sql

# Automatyczny backup (cron)
0 2 * * * /usr/bin/pg_dump -U kodkids kids_coding_platform > /backups/db_$(date +\%Y\%m\%d).sql
```

### Database Restore

```bash
psql -U kodkids kids_coding_platform < backup_20241107.sql
```

---

## Rozwiązywanie Problemów

### Problem: Backend nie startuje

```bash
# Sprawdzenie logów
docker-compose logs backend

# Lub bezpośrednio
tail -f /var/log/kodkids/django.log
```

### Problem: Błąd połączenia z bazą danych

```bash
# Test połączenia
psql -U kodkids -h localhost kids_coding_platform

# Sprawdzenie czy PostgreSQL działa
sudo systemctl status postgresql
```

### Problem: RabbitMQ nie działa

```bash
# Restart
sudo systemctl restart rabbitmq-server

# Sprawdzenie statusu
sudo rabbitmqctl status

# Sprawdzenie kolejek
sudo rabbitmqctl list_queues
```

### Problem: Frontend nie łączy się z API

1. Sprawdź CORS w Django settings
2. Sprawdź REACT_APP_API_URL w .env
3. Sprawdź czy backend jest dostępny: `curl http://localhost:8000/api/`

---

## Migracja Danych

### Export danych

```bash
python manage.py dumpdata > full_backup.json
python manage.py dumpdata api.User > users.json
python manage.py dumpdata api.Course api.Lesson > courses.json
```

### Import danych

```bash
python manage.py loaddata full_backup.json
```

---

## Kontakt i Wsparcie

**Dokumentacja**: https://docs.kodkids.pl
**GitHub Issues**: https://github.com/your-org/kodkids-platform/issues
**Email**: support@kodkids.pl

---

*Ostatnia aktualizacja: Listopad 2024*