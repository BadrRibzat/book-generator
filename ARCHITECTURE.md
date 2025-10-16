# Book Generator SaaS - Complete Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Auth (Register/Login)                                        │
│           ↓                                                       │
│  2. Configure Book (Domain → Sub-niche → Page Count)            │
│           ↓                                                       │
│  3. System Auto-generates Title                                  │
│           ↓                                                       │
│  4. Content Generation (Groq LLM → PDF Interior)                │
│           ↓                                                       │
│  5. ⚠️  MANDATORY: Cover Selection Phase                         │
│     - System generates 3 cover options                           │
│     - User MUST select one (or regenerate)                       │
│     - Download blocked until cover selected                      │
│           ↓                                                       │
│  6. PDF Assembly (Cover + Interior → Final Book)                │
│           ↓                                                       │
│  7. ✅ Download Button Appears                                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Tech Stack (100% Free - No Credit Card Required)

### Backend
- **Framework**: Django 4.2 + Django REST Framework
- **Database**: 
  - SQLite (metadata, user accounts)
  - MongoDB Atlas Free Tier (book content storage)
- **LLM**: Groq (Llama 3.1 70B / Mixtral) - Free tier
- **PDF Generation**: 
  - ReportLab (interior formatting)
  - WeasyPrint (HTML/CSS → PDF for covers)
  - pypdf (PDF merging)
- **Cover Design**: HTML/CSS templates (no external API needed)
- **Auth**: Django Session Authentication (no JWT libs needed)

### Frontend (Future Implementation)
- Vue 3 + TypeScript
- DaisyUI (Tailwind CSS)
- Axios for API calls

### Storage
- Local filesystem (development)
- Cloudflare R2 (production - free tier)

### Async Tasks
- Can use Django-Q + Redis (optional)
- Currently synchronous for simplicity

## Database Schema

### SQLite (Django Models)

#### Book Model
```python
- id (PK)
- user (FK → User)
- title (auto-generated)
- domain (choice: health, food, personal_dev, hobbies, lifestyle)
- sub_niche (15 choices mapped to domains)
- page_length (15, 20, 25, 30)
- status (draft, generating, content_generated, cover_pending, ready, error)
- mongodb_id (reference to MongoDB content)
- created_at, updated_at, content_generated_at, completed_at
- error_message
```

#### Cover Model
```python
- id (PK)
- book (FK → Book)
- template_style (modern, bold, elegant)
- image_path (PNG preview)
- pdf_path (PDF version for merging)
- is_selected (boolean)
- generation_params (JSON: colors, fonts, etc.)
- created_at
```

### MongoDB Collections

#### book_contents
```json
{
  "_id": ObjectId,
  "book_id": integer,
  "content": {
    "chapters": [
      {
        "title": "Chapter 1: ...",
        "content": ["paragraph1", "paragraph2", ...]
      }
    ],
    "total_chapters": integer
  },
  "interior_pdf_path": "/path/to/interior.pdf",
  "final_pdf_path": "/path/to/final.pdf",
  "created_at": ISO datetime
}
```

## API Endpoints

### Authentication
```
POST /api/auth/register/
  Body: { username, email, password, password2 }
  Response: { user: {...}, message }

POST /api/auth/login/
  Body: { username, password }
  Response: { user: {...}, message }

POST /api/auth/logout/
  Response: { message }

GET /api/auth/me/
  Response: { id, username, email }
```

### Configuration
```
GET /api/config/sub-niches/
  Response: {
    domains: [{value, label}],
    sub_niches: {
      health: [{value, label}, ...],
      ...
    },
    page_lengths: [15, 20, 25, 30]
  }
```

### Book Management
```
POST /api/books/
  Body: { domain, sub_niche, page_length }
  Response: Book object (status: "generating")
  
GET /api/books/
  Response: [List of user's books]
  
GET /api/books/{id}/
  Response: {
    id, title, domain, sub_niche, page_length, status,
    covers: [
      { id, template_style, image_url, is_selected }
    ],
    selected_cover: {...} or null,
    can_download: boolean,
    download_url: string or null
  }

POST /api/books/{id}/select_cover/
  Body: { cover_id }
  Response: Updated book object (status: "ready")

POST /api/books/{id}/regenerate_covers/
  Response: Book object with new covers

GET /api/books/{id}/download/
  Response: PDF file (only if status="ready" and cover selected)

POST /api/books/{id}/regenerate_content/
  Response: Book object (restarts generation)

GET /api/books/history/
  Response: [List of all user books]

DELETE /api/books/history/
  Response: 204 No Content
```

## Status Flow

```
draft
  ↓ (POST /api/books/)
generating
  ↓ (Groq LLM generates content)
content_generated
  ↓ (System auto-generates 3 covers)
cover_pending ⚠️  USER MUST TAKE ACTION
  ↓ (POST /api/books/{id}/select_cover/)
ready ✅ (Download available)
```

## Sub-Niches (15 Total)

### Health & Wellness (3)
1. yoga_beginners - "Yoga for Beginners"
2. home_workouts - "Home Workouts"
3. mental_wellness - "Mental Wellness"

### Food & Nutrition (3)
4. vegan_recipes - "Vegan Recipes"
5. meal_prep - "Meal Prep Guide"
6. smoothie_recipes - "Smoothie Recipes"

### Personal Development (3)
7. productivity - "Productivity Hacks"
8. morning_routines - "Morning Routines"
9. goal_setting - "Goal Setting"

### Hobbies & Crafts (3)
10. gardening - "Home Gardening"
11. photography - "Photography Basics"
12. diy_crafts - "DIY Crafts"

### Lifestyle (3)
13. minimalism - "Minimalist Living"
14. sustainable_living - "Sustainable Living"
15. travel_hacks - "Travel Hacks"

## Cover Generation

### Template Styles
1. **Modern**: Minimalist with geometric shapes, gradient backgrounds
2. **Bold**: Typography-focused, high contrast
3. **Elegant**: Serif fonts, border frames, professional

### Niche-Specific Colors
Each sub-niche has a custom color scheme:
- Primary (main background/text)
- Secondary (accents)
- Accent (highlights)

Example:
```python
'yoga_beginners': {
  'primary': '#4A90E2',  # Calming blue
  'secondary': '#7ED321',  # Fresh green
  'accent': '#F8E71C'  # Energetic yellow
}
```

### Process
1. Generate HTML with embedded CSS
2. Render to PDF using WeasyPrint (6"x9" book size)
3. Convert to PNG for web preview
4. Store both versions

## PDF Assembly

### Interior PDF (ReportLab)
- Professional typography
- Title page
- Chapter breaks
- Justified text
- Page numbers
- Proper margins

### Final PDF (pypdf merger)
```python
1. Load cover PDF (first page)
2. Load interior PDF (all pages)
3. Merge: [cover] + [interior pages]
4. Save as final downloadable PDF
```

## Directory Structure

```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── utils/
│       └── mongodb.py
├── books/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── services/
│       ├── book_generator.py
│       └── pdf_merger.py
├── covers/
│   ├── models.py
│   ├── serializers.py
│   ├── services.py
│   └── admin.py
└── media/
    ├── books/
    │   ├── book_1_interior.pdf
    │   └── book_1_final.pdf
    └── covers/
        ├── book_1_modern_1234.png
        ├── book_1_modern_1234.pdf
        ├── book_1_bold_5678.png
        └── ...
```

## Environment Variables (.env)

```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB Atlas (Free Tier)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=book_generator_db

# Groq API (Free Tier)
GROQ_API_KEY=gsk_...your-key...

# Optional: Redis (for async tasks)
# REDIS_URL=redis://localhost:6379/0
```

## Key Features

### ✅ Implemented
1. **Session-based auth** (no JWT dependency)
2. **15 sub-niches** across 5 domains
3. **Auto-title generation** (market-optimized)
4. **LLM content generation** (Groq free tier)
5. **3 cover template styles** (HTML/CSS, no external API)
6. **Niche-specific color schemes**
7. **PDF assembly** (cover + interior)
8. **Download blocking** until cover selected
9. **Book history** with regenerate options
10. **Error handling** and status tracking

### 🚀 Production Readiness
- All services use free tiers
- No credit card required
- MongoDB Atlas: 512MB free
- Groq: Generous free limits
- WeasyPrint: Open source
- Can scale to paid tiers later

## Testing the API

### 1. Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }' \
  -c cookies.txt
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }' \
  -c cookies.txt
```

### 3. Create Book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "domain": "health",
    "sub_niche": "yoga_beginners",
    "page_length": 20
  }'
```

### 4. Check Status
```bash
curl http://localhost:8000/api/books/1/ -b cookies.txt
```

### 5. Select Cover
```bash
curl -X POST http://localhost:8000/api/books/1/select_cover/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"cover_id": 1}'
```

### 6. Download Book
```bash
curl http://localhost:8000/api/books/1/download/ \
  -b cookies.txt \
  -o my-book.pdf
```

## Deployment Checklist

### Pre-Deployment
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS
- [ ] Generate strong SECRET_KEY
- [ ] Verify MongoDB connection
- [ ] Test Groq API key
- [ ] Run collectstatic

### Platform Options (Free Tier)
1. **Railway.app** - Generous free tier
2. **Fly.io** - Free tier with auto-sleep
3. **PythonAnywhere** - Free tier for Django
4. **Render** - Free tier (sleeps after inactivity)

### Production Settings
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Future Enhancements

1. **Async Task Queue** (Django-Q + Redis)
2. **Email notifications** when book ready
3. **Frontend UI** (Vue 3 + TypeScript)
4. **Book previews** (first 3 pages)
5. **Custom cover uploads**
6. **More sub-niches**
7. **Multi-language support**
8. **Payment integration** (for premium features)

## License
MIT License

## Support
For issues or questions, open a GitHub issue.
