# Learnova LMS - Project Structure

Industry-level Learning Management System built with Django REST Framework.

## Folder Structure

```
Learnova-production/
├── config/                 # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/               # Shared utilities & validators
│   │   ├── validators.py   # Common validation functions
│   │   ├── serializers.py  # Base serializers & mixins
│   │   ├── exceptions.py   # Custom exception handlers
│   │   └── permissions.py  # Reusable permission classes
│   ├── users/              # User management (Admin, Instructor, Student)
│   ├── courses/            # Courses, modules, lessons
│   ├── enrollments/        # Student enrollments & progress
│   ├── assessments/        # Quizzes, exams, assignments
│   ├── attendance/         # Live sessions & attendance
│   ├── communications/     # Announcements
│   └── analytics/          # Reports & dashboards
├── templates/
├── media/
├── staticfiles/
├── manage.py
└── requirements.txt
```

## Common Validators (`apps/core/validators.py`)

| Validator | Purpose |
|-----------|---------|
| `validate_email_format` | Email validation |
| `validate_phone_format` | Phone number format |
| `validate_slug_format` | URL slug (lowercase, hyphens) |
| `validate_username_format` | Username rules |
| `validate_future_date` | Date must be future |
| `validate_percentage` | 0-100 range |
| `validate_file_size` | Max file size (MB) |
| `validate_quiz_time_limit` | Quiz duration (1-480 min) |

## API Endpoints

### Auth (`/api/v1/auth/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `token/` | Login (get JWT) |
| POST | `token/refresh/` | Refresh JWT |
| POST | `users/` | Register new user |
| GET/PUT/PATCH | `users/me/` | Current user profile |
| GET | `users/` | List users (Admin) |
| GET/PUT/PATCH/DELETE | `users/<id>/` | User CRUD (Admin) |

### Courses (`/api/v1/courses/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `categories/` | Course categories |
| GET/POST | `` | Course library (students see published only) |
| GET/PUT/PATCH/DELETE | `<id>/` | Course detail |
| GET/POST | `modules/` | Modules |
| GET/POST | `lessons/` | Lessons |
| *Query* | `?status=PUBLISHED` | Filter by status |

### Enrollments (`/api/v1/enrollments/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `` | My enrollments (filtered by role) |
| POST | `enroll/` | Enroll in course `{course_id: 1}` |
| GET | `my-courses/` | Student dashboard - my courses + progress |
| GET/POST | `lesson-progress/` | Lesson completion tracking |
| GET | `certificates/` | My certificates (Progress & Certificate section) |

### Assessments (`/api/v1/assessments/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `quizzes/` | Quizzes & exams |
| GET/POST | `quiz-attempts/` | Quiz attempts |
| GET/POST | `assignments/` | Assignments |
| GET/POST | `submissions/` | Assignment submissions |

### Attendance (`/api/v1/attendance/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `sessions/` | Live sessions |
| GET/POST | `` | Attendance records |

### Communications (`/api/v1/communications/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `announcements/` | Announcements |

### Analytics (`/api/v1/analytics/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `dashboard/overview/` | Admin dashboard metrics |
| GET | `dashboard/instructor/students/` | Instructor: Students in my courses `?course_id=1` |
| GET/POST | `reports/` | Reports (Admin) |

## User Roles

- **Admin**: Full system control, user management, course moderation, analytics
- **Instructor**: Create courses, manage content, grade assignments, track students
- **Student**: Enroll, consume content, submit assignments, take quizzes

## Setup

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables

- `DJANGO_SECRET_KEY` - Secret key (required in production)
- `DEBUG` - True/False
- `DB_ENGINE` - sqlite (default) or postgresql
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - For PostgreSQL
