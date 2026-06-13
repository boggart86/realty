# ЧелРеалти

SSR Django-проект с PostgreSQL, Gunicorn и Nginx в Docker.

## Стек
- **Backend:** Django 5.0, PostgreSQL 16
- **Frontend:** Bootstrap 5, шрифты Inter + Playfair Display
- **Инфраструктура:** Docker Compose, Gunicorn, Nginx

## Быстрый старт

### 1. Клонируйте / распакуйте проект

```bash
cd chel_realty
```

### 2. Создайте `.env` из примера

```bash
cp .env.example .env
```

Отредактируйте `.env` — обязательно смените `SECRET_KEY` и пароль БД:

```env
SECRET_KEY=измените-на-случайный-ключ
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=chel_realty
DB_USER=chel_user
DB_PASSWORD=сложный_пароль
DB_HOST=db
DB_PORT=5432
```

### 3. Запустите проект

```bash
docker compose up -d --build
```

При первом запуске автоматически выполнятся:
- `migrate` — создание таблиц
- `collectstatic` — сборка статики


### 4. Создайте суперпользователя

```bash
docker compose exec web python manage.py createsuperuser
```
#### добавление тестовых данных

```bash
docker-compose exec web python manage.py loaddata properties
```

Введите email и пароль.

### 5. Откройте браузер

- **Сайт:** http://localhost
- **Админ-панель:** http://localhost/admin

---

## Роли пользователей

| Роль | Возможности |
|---|---|
| Гость | Просмотр каталога с фильтрами |
| Зарегистрированный | + Избранное |
| Персонал (`is_staff=True`) | + Добавление/редактирование/удаление **своих** объектов, ссылка на Admin |
| Суперпользователь | + Управление **любыми** объектами |

### Сделать пользователя персоналом

Через админ-панель: выставить флаг `is_staff`.

Или через shell:
```bash
docker compose exec web python manage.py shell -c "
from apps.users.models import User
u = User.objects.get(email='user@example.com')
u.is_staff = True
u.save()
"
```

---

## Структура проекта

```
chel_realty/
├── apps/
│   ├── users/          # Авторизация (email + пароль)
│   └── realty/         # Объекты, фото, избранное
├── config/             # settings.py, urls.py, wsgi.py
├── nginx/              # nginx.conf
├── static/             # CSS, JS
├── templates/          # base.html
├── media/              # Загруженные фото (volume)
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Полезные команды

```bash
# Логи
docker compose logs -f web

# Остановить
docker compose down

# Остановить + удалить volumes (осторожно: удалит БД и медиафайлы)
docker compose down -v

# Django shell
docker compose exec web python manage.py shell

# Применить миграции вручную
docker compose exec web python manage.py migrate
```

---

## Настройки

В `config/settings.py`:
- `MAX_PHOTO_SIZE = 30 * 1024 * 1024` — максимальный размер одного фото (30 МБ)
- `MAX_PHOTOS_PER_REALTY = 10` — максимум фото на объект
- `REALTY_PER_PAGE = 9` — объектов на страницу каталога
