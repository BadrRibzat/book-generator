# BookAI Backend - Development Setup

## 🚀 Quick Start (Auto-start Everything)

### The Easy Way - One Command
```bash
cd /home/badr/book-generator/backend
./start_dev.sh
```

This automatically starts:
- ✅ Redis (if not running)
- ✅ Celery Worker (background)
- ✅ Django Server (foreground)

### Stop Everything
```bash
./stop_dev.sh
```

### Check Service Status
```bash
./status_dev.sh
```

---

## 📋 What You Need to Know

### Why You Need Celery Running

**Django Server** handles HTTP requests (API endpoints)
**Celery Worker** handles async background tasks:
- 📝 Book content generation (2-3 minutes)
- 🎨 Cover generation with AI
- 📄 PDF creation and merging

**Without Celery running:**
- ❌ Books stuck at 0% "Initializing..."
- ❌ Progress never updates
- ❌ Tasks queued but never processed

**With Celery running:**
- ✅ Real-time progress updates (0% → 100%)
- ✅ Background AI generation
- ✅ Automatic cover creation
- ✅ Final PDF assembly

---

## 🔧 Manual Control (Advanced)

### Start Services Individually

1. **Start Redis** (if not running):
```bash
sudo service redis-server start
redis-cli ping  # Should return PONG
```

2. **Start Celery Worker**:
```bash
cd /home/badr/book-generator/backend
celery -A backend worker --loglevel=info
```

3. **Start Django Server** (separate terminal):
```bash
cd /home/badr/book-generator/backend
python manage.py runserver
```

### View Logs

**Celery Worker Logs** (when using start_dev.sh):
```bash
tail -f celery_worker.log
```

**Celery Worker Logs** (manual start - in terminal):
```bash
# Output appears in the terminal where you started Celery
```

**Django Server Logs**:
```bash
# Output appears in the terminal where you started runserver
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Vue.js)                    │
│              http://localhost:5173                       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Django Server (Port 8000)                   │
│  • API Endpoints: /api/books/, /api/domains/, etc.      │
│  • Creates Book record                                   │
│  • Triggers Celery task: generate_book_content.delay()  │
└────────────────────┬────────────────────────────────────┘
                     │ Task Queue
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Redis (Port 6379)                      │
│            Message Broker / Task Queue                   │
└────────────────────┬────────────────────────────────────┘
                     │ Picks up tasks
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Celery Worker                           │
│  • Processes background tasks                            │
│  • Updates book.progress_percentage (0% → 100%)         │
│  • Updates book.current_step (status messages)          │
│  • Calls AI APIs (OpenRouter)                           │
│  • Generates PDFs                                        │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Task Pipeline

When a user creates a book, these tasks run **in sequence**:

### Task 1: `generate_book_content(book_id)`
**Duration:** 90-120 seconds  
**Progress:** 10% → 90%

Steps:
1. ✅ Initialize (10%)
2. 📝 Generate outline with MiniMax M2 (20%)
3. 📖 Generate chapters with NVIDIA Nemotron (60%)
4. 🔍 Review content with Mistral Small (optional, 70%)
5. 📄 Create interior PDF (80%)
6. 💾 Store in MongoDB (90%)

**Result:** Book status → `content_generated`

---

### Task 2: `generate_book_covers(book_id)`
**Duration:** 20-30 seconds  
**Progress:** 92% → 98%

Steps:
1. 🎨 Generate cover brief (92%)
2. 🖼️ Create cover with Cloudflare AI (94%)
3. 💾 Save cover image (98%)

**Result (Guided):** Auto-select cover → Trigger Task 3  
**Result (Manual):** Book status → `cover_pending` (user selects)

---

### Task 3: `create_final_book_pdf(book_id)`
**Duration:** 5-10 seconds  
**Progress:** 98% → 100%

Steps:
1. 📑 Merge cover + interior PDF (99%)
2. 💾 Save final book (100%)

**Result:** Book status → `ready` ✅

---

## 🐛 Troubleshooting

### Problem: Books Stuck at 0% "Initializing..."

**Diagnosis:**
```bash
./status_dev.sh
```

Look for:
```
Celery Worker Status:
  ✗ Not Running
```

**Solution:**
```bash
./start_dev.sh
```

---

### Problem: "Connection refused" Error

**Diagnosis:**
```bash
redis-cli ping
```

If no response:
```bash
sudo service redis-server start
```

---

### Problem: Tasks Not Processing

**Check Celery Worker Logs:**
```bash
tail -f celery_worker.log
```

Look for:
- ✅ `[INFO/MainProcess] Connected to redis://...`
- ✅ `[INFO/MainProcess] celery@... ready`
- ❌ Connection errors
- ❌ Task failures

**Restart Celery:**
```bash
./stop_dev.sh
./start_dev.sh
```

---

### Problem: Progress Stuck at Specific Percentage

**Check Task Status:**
```bash
# Check current tasks in queue
redis-cli -n 0 LLEN celery

# Monitor Celery worker output
tail -f celery_worker.log | grep "Task.*book"
```

**Common Issues:**
- 🔑 **API Key Error**: Check OpenRouter API key in `.env`
- 💾 **MongoDB Error**: Check MongoDB connection
- 📁 **File Permission**: Check media folder permissions

---

## 🔍 Monitoring Progress

### Real-time Book Status

**In Browser:**
1. Navigate to book details page
2. Progress automatically polls every 3 seconds
3. Shows:
   - Progress bar (0% → 100%)
   - Current step text
   - Estimated time remaining

**In Database:**
```bash
python manage.py shell -c "
from books.models import Book
book = Book.objects.latest('id')
print(f'Status: {book.status}')
print(f'Progress: {book.progress_percentage}%')
print(f'Step: {book.current_step}')
"
```

**In Redis Queue:**
```bash
# Check pending tasks
redis-cli -n 0 LLEN celery
```

---

## 📦 Dependencies

### Required Services
- **Redis**: Message broker for Celery
- **Python 3.12+**: Django and Celery
- **MongoDB**: Book content storage

### Python Packages
```bash
pip install celery redis django-celery-results django-celery-beat
```

Already in `requirements.txt` ✅

### PDF → PNG Previews

The backend converts generated cover PDFs to PNG previews. Two backends are supported:

- pdf2image (requires system Poppler)
- PyMuPDF (pure Python; no system deps)

Out of the box we use PyMuPDF as a fallback so previews work even if Poppler isn't installed.

Optional (Linux): Install Poppler for faster pdf2image rendering

```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

Python packages used:

- pdf2image (already included)
- PyMuPDF (already included)
- Pillow (already included)

If pdf2image fails due to missing Poppler, the logs will suggest installing `poppler-utils` and will automatically fall back to PyMuPDF.

---

## 🎯 Best Practices

### Development Workflow

1. **Start Services:**
```bash
cd /home/badr/book-generator/backend
./start_dev.sh
```

2. **Develop & Test:**
- Django server logs in terminal
- Celery logs in `celery_worker.log`
- Monitor with `./status_dev.sh`

3. **Stop Services:**
```bash
./stop_dev.sh
```

### Production Deployment

For production, use:
- **Supervisor** or **systemd** to manage Celery
- **Gunicorn** or **uWSGI** for Django
- **Nginx** as reverse proxy
- Multiple Celery workers for parallel processing

---

## 🔐 Environment Variables

Required in `.env` or `backend/settings.py`:

```env
# OpenRouter API (for AI generation)
OPENROUTER_API_KEY=sk-or-v1-...

# Cloudflare AI (for cover generation)
CLOUDFLARE_ACCOUNT_ID=your-account-id
CLOUDFLARE_API_TOKEN=your-api-token

# Celery (already configured)
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0

# MongoDB (for content storage)
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=bookgen
```

---

## 📈 Performance Tuning

### Increase Celery Workers
```bash
celery -A backend worker --loglevel=info --concurrency=4
```

Default is CPU count. Increase for more parallel book generation.

### Monitor Queue Length
```bash
watch -n 1 'redis-cli -n 0 LLEN celery'
```

If queue grows, add more workers or optimize tasks.

---

## ✅ Verification Checklist

After starting services, verify:

- [ ] Redis responds: `redis-cli ping` → `PONG`
- [ ] Celery worker running: `./status_dev.sh` shows ✓
- [ ] Django server accessible: `curl http://127.0.0.1:8000/`
- [ ] Create test book: Progress goes 0% → 100%
- [ ] Check logs: No errors in `celery_worker.log`

---

## 🎓 Learning Resources

**Celery Basics:**
- Why async tasks: http://www.celeryproject.org/
- Task queues explained: https://docs.celeryproject.org/en/stable/getting-started/introduction.html

**Redis as Broker:**
- Why Redis: https://docs.celeryproject.org/en/stable/getting-started/backends-and-brokers/redis.html

---

## 🆘 Quick Help

| Command | Purpose |
|---------|---------|
| `./start_dev.sh` | Start everything (Redis + Celery + Django) |
| `./stop_dev.sh` | Stop Celery + Django |
| `./status_dev.sh` | Check what's running |
| `tail -f celery_worker.log` | Watch Celery logs |
| `redis-cli ping` | Test Redis connection |
| `ps aux \| grep celery` | Find Celery processes |
| `pkill -f celery` | Kill all Celery workers |

---

**Now you can run everything with one command!** 🚀

```bash
./start_dev.sh
```
