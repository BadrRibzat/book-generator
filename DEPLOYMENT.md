# Deployment Guide - Book Generator SaaS

## Overview
This guide covers deploying your book generator to production using **100% free services** that require **NO credit card or payment method**.

---

## Prerequisites

✅ **Completed Setup**
- Backend running locally
- MongoDB Atlas account (free)
- Groq API key (free)
- Git repository

---

## Option 1: Railway.app (Recommended)

### Why Railway?
- 500 hours free per month
- Easy PostgreSQL/Redis integration
- Automatic deployments from GitHub
- No credit card required initially

### Steps

#### 1. Prepare Your Project

Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn backend.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:
```
web: gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
```

Update `requirements.txt`:
```bash
cd /home/badr/book-generator/backend
source venv/bin/activate
pip install gunicorn whitenoise
pip freeze > requirements.txt
```

#### 2. Update Django Settings

Add to `backend/settings.py`:
```python
import dj_database_url

# Production settings
if not DEBUG:
    # WhiteNoise for static files
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Allow Railway domain
    ALLOWED_HOSTS.append('.railway.app')
    
    # Database (Railway PostgreSQL - optional)
    # Keep SQLite for now, or use Railway's PostgreSQL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
```

#### 3. Deploy to Railway

1. Sign up at https://railway.app (use GitHub OAuth - no card needed)
2. Create new project → "Deploy from GitHub repo"
3. Select your repository
4. Railway auto-detects Django
5. Add environment variables:
   - `SECRET_KEY` → (generate new: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG` → `False`
   - `ALLOWED_HOSTS` → `*` (or specific domain)
   - `GROQ_API_KEY` → your key
   - `MONGODB_URI` → your MongoDB Atlas URI
   - `MONGODB_DB_NAME` → `book_generator_db`
6. Click "Deploy"
7. Railway provides a URL: `https://your-app.railway.app`

---

## Option 2: Render.com

### Why Render?
- 750 hours free per month
- PostgreSQL included (free tier)
- Automatic HTTPS
- No credit card for free tier

### Steps

#### 1. Create `render.yaml`
```yaml
services:
  - type: web
    name: book-generator
    env: python
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
    startCommand: "gunicorn backend.wsgi:application"
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: GROQ_API_KEY
        sync: false
      - key: MONGODB_URI
        sync: false
      - key: MONGODB_DB_NAME
        value: book_generator_db
```

#### 2. Deploy

1. Sign up at https://render.com (GitHub OAuth - no card)
2. New → Web Service
3. Connect GitHub repo
4. Render auto-detects settings
5. Add environment variables (same as Railway)
6. Click "Create Web Service"
7. URL: `https://your-app.onrender.com`

⚠️ **Note**: Free tier sleeps after 15 min inactivity (first request takes 30s to wake)

---

## Option 3: PythonAnywhere

### Why PythonAnywhere?
- Always-on (no sleeping)
- Beginner-friendly
- Free tier includes MySQL
- No credit card required

### Steps

#### 1. Sign Up
- Go to https://www.pythonanywhere.com
- Create free account (no card needed)
- Free tier: `yourusername.pythonanywhere.com`

#### 2. Upload Code
```bash
# On PythonAnywhere bash console:
git clone https://github.com/yourusername/book-generator.git
cd book-generator/backend
mkvirtualenv --python=python3.10 bookgen
pip install -r requirements.txt
```

#### 3. Configure Web App
1. Web tab → Add new web app
2. Manual configuration → Python 3.10
3. Virtualenv: `/home/yourusername/.virtualenvs/bookgen`
4. WSGI file:
```python
import sys
import os

path = '/home/yourusername/book-generator/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

5. Static files mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/book-generator/backend/static`

6. Media files mapping:
   - URL: `/media/`
   - Directory: `/home/yourusername/book-generator/backend/media`

#### 4. Environment Variables
Create `.env` in `/home/yourusername/book-generator/backend/`:
```bash
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
GROQ_API_KEY=your-key
MONGODB_URI=your-mongodb-uri
MONGODB_DB_NAME=book_generator_db
```

#### 5. Reload
- Click "Reload" button on Web tab
- Visit `https://yourusername.pythonanywhere.com`

⚠️ **Limitations**: 
- CPU seconds limited (book generation might timeout)
- Not ideal for long LLM operations

---

## Option 4: Fly.io

### Why Fly.io?
- Generous free tier
- Great for Dockerized apps
- Global edge deployment

### Steps

#### 1. Install Fly CLI
```bash
curl -L https://fly.io/install.sh | sh
flyctl auth signup  # No card required
```

#### 2. Create `Dockerfile`
```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD python manage.py migrate && \
    gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

#### 3. Create `fly.toml`
```toml
app = "book-generator"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

#### 4. Deploy
```bash
cd /home/badr/book-generator/backend
flyctl launch  # Follow prompts
flyctl secrets set SECRET_KEY=your-key
flyctl secrets set GROQ_API_KEY=your-key
flyctl secrets set MONGODB_URI=your-uri
flyctl secrets set MONGODB_DB_NAME=book_generator_db
flyctl deploy
```

---

## Production Checklist

### Security
- [ ] `DEBUG=False`
- [ ] Strong `SECRET_KEY` (never commit to Git)
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] HTTPS enabled (automatic on Railway/Render/Fly)
- [ ] `SECURE_SSL_REDIRECT=True` (if HTTPS)
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`

### Database
- [ ] MongoDB Atlas whitelisted IP (0.0.0.0/0 for flexibility)
- [ ] Regular backups enabled
- [ ] Connection string uses SRV format

### Static/Media Files
- [ ] `collectstatic` runs on deploy
- [ ] Media files persistent (use volume/S3 for Railway)
- [ ] WhiteNoise configured for static files

### Monitoring
- [ ] Error logging configured
- [ ] Health check endpoint (optional)
- [ ] Sentry integration (optional)

### Performance
- [ ] Gunicorn workers: `2-4 * CPU_CORES`
- [ ] Request timeout: 300s (for LLM operations)
- [ ] Database connection pooling

---

## Environment Variables Summary

**Required for all platforms:**
```bash
SECRET_KEY=<generate-new-one>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,*.railway.app
GROQ_API_KEY=gsk_...
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=book_generator_db
```

**Optional:**
```bash
REDIS_URL=redis://...  # If using async tasks
SENTRY_DSN=https://...  # If using error tracking
```

---

## Custom Domain (Optional)

### Railway/Render/Fly
1. Buy domain from Namecheap/Porkbun ($3-10/year)
2. Add CNAME record:
   - Name: `@` or `www`
   - Value: `your-app.railway.app` (or render/fly domain)
3. Add domain in platform settings
4. Wait for SSL provisioning (~5 min)

---

## Scaling (Future)

### When Free Tier Isn't Enough
1. **Railway Pro**: $5/month (more hours)
2. **Render Standard**: $7/month (always-on)
3. **AWS Lightsail**: $3.50/month (512MB VPS)
4. **DigitalOcean**: $4/month (droplet)

### Optimization Tips
- Cache LLM responses (MongoDB)
- Use Redis for session storage
- CDN for static/media files (Cloudflare R2)
- Background tasks (Celery/Django-Q)

---

## Troubleshooting

### "Application failed to start"
- Check logs: `railway logs` or `flyctl logs`
- Verify all env vars set
- Test locally with `DEBUG=False`

### "Static files not loading"
- Run `python manage.py collectstatic`
- Check WhiteNoise middleware order
- Verify `STATIC_ROOT` setting

### "MongoDB connection failed"
- Whitelist IP: 0.0.0.0/0
- Check URI format (SRV vs standard)
- Test connection with `pymongo` directly

### "Groq API errors"
- Verify API key is correct
- Check quota limits (free tier)
- Test with curl first

### "PDF generation timeout"
- Increase request timeout
- Consider async task queue
- Optimize LLM prompt length

---

## Post-Deployment Testing

```bash
# Replace with your domain
DOMAIN="https://your-app.railway.app"

# 1. Register user
curl -X POST $DOMAIN/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"demo1234","password2":"demo1234"}' \
  -c cookies.txt

# 2. Create book
curl -X POST $DOMAIN/api/books/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"domain":"health","sub_niche":"yoga_beginners","page_length":15}'

# 3. Check status (repeat until status="cover_pending")
curl $DOMAIN/api/books/1/ -b cookies.txt

# 4. Select cover
curl -X POST $DOMAIN/api/books/1/select_cover/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"cover_id":1}'

# 5. Download
curl $DOMAIN/api/books/1/download/ -b cookies.txt -o book.pdf
```

---

## Success Criteria

✅ **Your SaaS is production-ready when:**
1. API responds at public URL
2. User can register/login
3. Book generation completes end-to-end
4. Covers display correctly
5. Final PDF downloads successfully
6. No credit card was required for any service

---

## Support Resources

- **Railway**: https://railway.app/docs
- **Render**: https://render.com/docs
- **Fly.io**: https://fly.io/docs
- **PythonAnywhere**: https://help.pythonanywhere.com
- **MongoDB Atlas**: https://www.mongodb.com/docs/atlas/
- **Groq**: https://console.groq.com/docs

---

## Next Steps

1. Choose deployment platform
2. Follow platform-specific steps above
3. Set environment variables
4. Deploy and test
5. Optional: Add custom domain
6. Build frontend (Vue 3)
7. Launch! 🚀
