# Environment Setup Guide

Learnova LMS uses environment variables for configuration. Use a `.env` file for local development.

## Quick Start

1. **Copy the example file:**
   ```bash
   copy .env.example .env
   ```
   (On Windows PowerShell: `Copy-Item .env.example .env`)

2. **Edit `.env`** with your values (optional for local dev – defaults work)

3. **Install dependencies** (includes python-dotenv):
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key. Generate a new one for production. | `dev-key-change-in-production` |
| `DEBUG` | Enable debug mode | `True` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `localhost,127.0.0.1` |
| `DB_ENGINE` | Database: `sqlite` or `postgresql` | `sqlite` |
| `DB_NAME` | PostgreSQL database name | `learnova_lms` |
| `DB_USER` | PostgreSQL user | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `postgres` |
| `DB_HOST` | PostgreSQL host | `localhost` |
| `DB_PORT` | PostgreSQL port | `5432` |

## Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Use a strong, unique `DJANGO_SECRET_KEY`
- [ ] Set `ALLOWED_HOSTS` to your domain(s)
- [ ] Use PostgreSQL (`DB_ENGINE=postgresql`) with secure credentials
- [ ] Never commit `.env` to version control (it's in `.gitignore`)

## Generating a Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
