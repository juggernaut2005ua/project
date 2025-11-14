# Frontend (Vite + React)

Минимальный фронтенд, который использует API бэкенда (Django REST Framework).

Как запустить локально:

1. Перейдите в папку `frontend`:

```bash
cd frontend
```

2. Установите зависимости и запустите dev-сервер:

```bash
npm install
npm run dev
```

3. Откройте в браузере URL, который покажет `vite` (обычно http://localhost:5173).

Настройки:
- По умолчанию `VITE_API_BASE_URL` может быть указана в `.env` или `import.meta.env.VITE_API_BASE_URL`. Пример: `VITE_API_BASE_URL=http://localhost:8000/api`.

Аутентификация:
- Клиент поддерживает заголовок Authorization: Bearer <token> (токен хранится в localStorage под `api_token`).

Дальше:
- Можно расширить UI, добавить роутер, страницы для Systems, Events, Mappings и т.д.
