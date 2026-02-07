# Deploy Learnova LMS (Django) on Vercel

Step-by-step guide to deploy your Django backend on Vercel.

---

## Prerequisites

- [Vercel account](https://vercel.com/signup)
- [GitHub](https://github.com) account (or GitLab/Bitbucket)
- Your Django project pushed to a Git repository
- PostgreSQL database (Vercel Postgres, Neon, or your own)

---

## Step 1: Push Code to GitHub

If not already done:

```bash
git add .
git commit -m "Add Vercel deployment config"
git push origin main
```

---

## Step 2: Import Project on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in.
2. Click **Add New** → **Project**.
3. Import your repository (GitHub/GitLab/Bitbucket).
4. Select the **Learnova-production** repository.

---

## Step 3: Configure Build Settings

Vercel should auto-detect Python. Use:

| Setting | Value |
|--------|-------|
| **Framework Preset** | Other |
| **Root Directory** | (leave empty – project root) |
| **Build Command** | `pip install -r requirements.txt && python manage.py collectstatic --noinput --clear` |
| **Output Directory** | (leave empty) |

---

## Step 4: Add Environment Variables

In **Project Settings** → **Environment Variables**, add:

| Variable | Value | Notes |
|----------|-------|-------|
| `DJANGO_SECRET_KEY` | (generate a strong random key) | Required |
| `DEBUG` | `False` | Always False in production |
| `ALLOWED_HOSTS` | `your-app.vercel.app,.vercel.app` | Your Vercel domain |
| `DB_ENGINE` | `postgresql` | |
| `DB_NAME` | Your DB name | From Vercel Postgres / Neon |
| `DB_USER` | Your DB user | |
| `DB_PASSWORD` | Your DB password | |
| `DB_HOST` | Your DB host | |
| `DB_PORT` | `5432` | |
| `CORS_ALLOW_ALL_ORIGINS` | `1` | Or set `CORS_ALLOWED_ORIGINS` to your frontend URL |

Generate a secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## Step 5: Run Migrations (Important)

Vercel serverless does not run migrations automatically. **Run them before first deploy** or right after:

1. **Option A – From your local machine** (with production DB URL in `.env`):

   ```bash
   python manage.py migrate
   ```

2. **Option B – Vercel Deploy Hook**  
   Add a pre-deploy script that runs migrations, or run migrations manually via Django admin / CLI after deploy.

---

## Step 6: Deploy

1. Click **Deploy**.
2. Wait for the build to finish.
3. Your API will be available at: `https://your-project.vercel.app`

---

## Step 7: Frontend (React)

Your React app is in `LogicLegend_frontend/`. Options:

### Option A: Deploy frontend on Vercel as a separate project

1. Create a new Vercel project.
2. Set **Root Directory** to `LogicLegend_frontend`.
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Add env var: `VITE_API_URL` = `https://your-django-api.vercel.app/api/v1`

### Option B: Monorepo – backend and frontend in one project

If you want both in one Vercel project, you need a custom config so that:

- `/api/*` goes to Django
- `/*` serves the React app

This needs a more advanced `vercel.json` (e.g. frontend as output, rewrites for API).

---

## API Endpoints After Deploy

- Base URL: `https://your-project.vercel.app`
- Auth: `https://your-project.vercel.app/api/v1/auth/`
- Courses: `https://your-project.vercel.app/api/v1/courses/`
- Enrollments: `https://your-project.vercel.app/api/v1/enrollments/`
- etc.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | Check build logs; ensure `requirements.txt` is correct. |
| 500 errors | Set `DEBUG=True` temporarily, check Vercel function logs. |
| DB connection fails | Verify env vars; for Vercel Postgres/Neon, ensure SSL/URL is correct. |
| CORS errors | Add your frontend URL to `CORS_ALLOWED_ORIGINS` or use `CORS_ALLOW_ALL_ORIGINS=1`. |
| Static files 404 | WhiteNoise serves them; confirm `collectstatic` runs in the build. |

---

## Notes

- Vercel runs Django as serverless functions (cold starts possible).
- For heavy workloads or WebSockets, consider Render, Railway, or Fly.io.
- Media uploads (e.g. thumbnails) need external storage (S3, Cloudinary) on Vercel; the filesystem is not persistent.
