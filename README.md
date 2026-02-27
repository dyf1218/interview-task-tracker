# Interview Task Tracker

A production-style backend demo built with **Django + Django REST Framework + PostgreSQL** for managing interview tasks with JWT authentication.

## Stack

- Python 3.11
- Django 5.1
- Django REST Framework 3.15
- djangorestframework-simplejwt 5.3
- PostgreSQL
- psycopg 3
- django-filter

## Features

- User registration and JWT authentication
- Task CRUD operations
- Per-user data isolation
- Filtering, search, and ordering
- Pagination
- Automated tests

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip

## Quick Start with Docker

The fastest way to run the project:

```bash
# Clone the repository
git clone https://github.com/dyf1218/interview-task-tracker.git
cd interview-task-tracker

# Start with Docker Compose
docker-compose up -d

# The API is now available at http://127.0.0.1:8000/
```

To stop the services:

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

---

## Manual Setup (Without Docker)

### 1. Create PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE interview_task_tracker;

# Exit
\q
```

### 2. Clone and Setup Virtual Environment

```bash
git clone https://github.com/dyf1218/interview-task-tracker.git
cd interview-task-tracker

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your database credentials
# - DB_NAME=interview_task_tracker
# - DB_USER=postgres
# - DB_PASSWORD=your_password
# - DB_HOST=127.0.0.1
# - DB_PORT=5432
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### 8. Run Tests

```bash
python manage.py test
```

## API Endpoints

### Authentication

| Method | Endpoint              | Description              |
| ------ | --------------------- | ------------------------ |
| POST   | `/api/auth/register/` | Register a new user      |
| POST   | `/api/auth/login/`    | Login and get JWT tokens |
| POST   | `/api/auth/refresh/`  | Refresh access token     |
| GET    | `/api/auth/me/`       | Get current user profile |

### Tasks

| Method | Endpoint           | Description                |
| ------ | ------------------ | -------------------------- |
| GET    | `/api/tasks/`      | List all tasks (paginated) |
| POST   | `/api/tasks/`      | Create a new task          |
| GET    | `/api/tasks/{id}/` | Get a specific task        |
| PUT    | `/api/tasks/{id}/` | Update a task (full)       |
| PATCH  | `/api/tasks/{id}/` | Update a task (partial)    |
| DELETE | `/api/tasks/{id}/` | Delete a task              |

### Query Parameters

| Parameter   | Example                 | Description                                |
| ----------- | ----------------------- | ------------------------------------------ |
| `status`    | `?status=todo`          | Filter by status (todo, in_progress, done) |
| `priority`  | `?priority=high`        | Filter by priority (low, medium, high)     |
| `search`    | `?search=django`        | Search in title                            |
| `ordering`  | `?ordering=-created_at` | Order by field                             |
| `page`      | `?page=1`               | Page number                                |
| `page_size` | `?page_size=10`         | Items per page (max 100)                   |

## Sample API Usage

### Register

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yufan",
    "email": "yufan@example.com",
    "password": "StrongPass123",
    "password_confirm": "StrongPass123"
  }'
```

Response:

```json
{
  "id": 1,
  "username": "yufan",
  "email": "yufan@example.com"
}
```

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "yufan",
    "password": "StrongPass123"
  }'
```

Response:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Create Task

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <access_token>" \
  -d '{
    "title": "Prepare Django interview demo",
    "description": "Finish auth, task CRUD and README",
    "status": "todo",
    "priority": "high",
    "due_date": "2026-02-28"
  }'
```

Response:

```json
{
  "id": 1,
  "title": "Prepare Django interview demo",
  "description": "Finish auth, task CRUD and README",
  "status": "todo",
  "priority": "high",
  "due_date": "2026-02-28",
  "created_at": "2026-02-27T10:00:00Z",
  "updated_at": "2026-02-27T10:00:00Z",
  "owner_id": 1
}
```

### List Tasks with Filters

```bash
# Filter by status
curl -X GET "http://127.0.0.1:8000/api/tasks/?status=todo" \
  -H "Authorization: Bearer <access_token>"

# Search by title
curl -X GET "http://127.0.0.1:8000/api/tasks/?search=django" \
  -H "Authorization: Bearer <access_token>"

# Order by created_at descending
curl -X GET "http://127.0.0.1:8000/api/tasks/?ordering=-created_at" \
  -H "Authorization: Bearer <access_token>"
```

### Get Current User

```bash
curl -X GET http://127.0.0.1:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

## Project Structure

```
interview-task-tracker/
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── apps/
    ├── __init__.py
    ├── users/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── urls.py
    │   └── tests.py
    └── tasks/
        ├── __init__.py
        ├── apps.py
        ├── models.py
        ├── serializers.py
        ├── permissions.py
        ├── filters.py
        ├── pagination.py
        ├── views.py
        ├── urls.py
        ├── admin.py
        └── tests.py
```

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials.

## License

This project is for interview demonstration purposes.
