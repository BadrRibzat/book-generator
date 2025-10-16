# 📚 Book Generator SaaS

> **Production-ready SaaS that generates complete, publish-ready digital books (15-30 pages + professional cover) in PDF format using AI - 100% FREE, no credit card required.**

![Status](https://img.shields.io/badge/status-ready-green)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![Django](https://img.shields.io/badge/django-4.2-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 🎯 What Is This?

A complete SaaS application that:
1. **Generates full book content** using Groq's free LLM API (Llama 3.1 70B)
2. **Creates 3 professional cover designs** using HTML/CSS templates
3. **Assembles everything into a single PDF** ready for download/publishing
4. **Requires NO payment method** - uses only free-tier services

### Key Features

✅ **15 Sub-Niches** across 5 domains (Health, Food, Personal Dev, Hobbies, Lifestyle)  
✅ **Auto-generated market-optimized titles**  
✅ **15-30 page books** with professional formatting  
✅ **3 cover styles** (Modern, Bold, Elegant) with niche-specific colors  
✅ **Mandatory cover selection** before download (ensures complete product)  
✅ **Book history** with regenerate/delete options  
✅ **Session-based auth** (no JWT complexity)  
✅ **MongoDB + SQLite** for efficient storage  
✅ **RESTful API** with 12+ endpoints  
✅ **100% free stack** - no credit card needed anywhere

---

## 🛠️ Tech Stack



## 🚀 Quick Start### Backend

- **Framework**: Django 4.2 + Django REST Framework

```bash- **Database**: SQLite (dev) → MongoDB Atlas (free tier, no credit card)

# 1. Clone & setup- **AI**: Groq API (Llama 3.1 8B, free tier)

git clone https://github.com/BadrRibzat/book-generator.git- **Async**: Django-Q (no Redis required)

cd book-generator/backend- **PDF**: WeasyPrint (HTML/CSS → print-ready PDF)

python -m venv venv

source venv/bin/activate### Frontend (Planned)

pip install -r requirements.txt- Vue 3 + TypeScript + Tailwind CSS + DaisyUI



# 2. Configure .env### Deployment (Planned)

cp .env.example .env- Backend: Render (free tier)

# Add: GROQ_API_KEY, MONGODB_URI, SECRET_KEY- Frontend: Vercel / Netlify

- Storage: Cloudflare R2 (free tier, no card)

# 3. Migrate & run

python manage.py migrate---

python manage.py runserver

## 🚦 Current Status

# 4. Test it works

python test_complete_flow.py✅ Backend project initialized  

```✅ User, Book, and Cover apps created  

✅ Groq API integration verified (`llama-3.1-8b-instant`)  

**Result**: `test_book_1.pdf` with cover + 15 pages of content!✅ Environment and dependency management ready  

✅ MIT Licensed  

---

> 🔜 Next: User authentication, book generation pipeline, and cover designer.

## 📖 User Flow

---

```

Register → Choose Niche → System Generates Title## 🧪 Test Groq Connection

    ↓

Content Generation (LLM creates chapters)```bash

    ↓cd backend

⚠️  MANDATORY: Select Cover (3 options)python test_groq.py

    ↓# Expected: "✅ Groq API connection successful!"

PDF Assembly (Cover + Interior)

    ↓📜 License

✅ Download Complete BookMIT © 2025 Badr Ribzat

```



------



## 🏗️ Tech Stack### ✅ Next Steps



| Component | Technology | Cost |Run these commands to commit and push:

|-----------|-----------|------|

| Backend | Django 4.2 + DRF | Free |```bash

| Database | SQLite + MongoDB Atlas | Free |# Add README

| LLM | Groq (Llama 3.1 70B) | Free |echo "# Book Generator SaaS

| PDF | ReportLab + WeasyPrint | Free (OSS) |

| Covers | HTML/CSS Templates | Free |A credit-card-free, open-source SaaS platform that generates **complete, publish-ready digital books** (15–30 pages + professional cover) in PDF format using AI. Built for creators, educators, and indie publishers who want high-quality, niche-targeted books in seconds — with zero upfront cost.

| Deployment | Railway/Render/Fly.io | Free Tier |

> 🚀 **No bank account or payment method required** — built entirely with free-tier tools.

---

---

## 🎨 15 Sub-Niches

## ✨ Features

**Health & Wellness**: Yoga • Home Workouts • Mental Wellness  

**Food & Nutrition**: Vegan Recipes • Meal Prep • Smoothies  - **Niche-Optimized Content**: Choose from 15 evergreen sub-niches across 5 domains:

**Personal Dev**: Productivity • Morning Routines • Goal Setting    - 📚 Language & Kids (e.g., personalized learning stories)

**Hobbies & Crafts**: Gardening • Photography • DIY    - 💻 Technology & AI (e.g., no-code guides, AI ethics)

**Lifestyle**: Minimalism • Sustainable Living • Travel Hacks  - 🥑 Nutrition & Wellness (e.g., keto cookbooks, mental health nutrition)

  - 🧘 Meditation (e.g., anxiety workbooks, gratitude journals)

Each with custom colors + 3 cover styles (Modern/Bold/Elegant).  - 💪 Home Workout (e.g., desk yoga, bodyweight plans)

- **Auto-Generated Titles**: Market-optimized titles for better discoverability.

---- **Professional Covers**: 3 AI-assisted cover options per book (template-based).

- **Complete PDF Output**: Interior + cover merged into one downloadable file.

## 📡 API Documentation

### 🎯 Interactive Documentation (Swagger/ReDoc)

**NEW!** Professional interactive API documentation:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/ 
  - Try all endpoints directly in browser
  - Test authentication flow
  - See request/response examples
  - Built-in API testing

- **ReDoc:** http://127.0.0.1:8000/api/redoc/
  - Beautiful, responsive documentation
  - Printable format
  - Search functionality

- **OpenAPI Schema:** http://127.0.0.1:8000/api/schema/
  - Import into Postman/Insomnia
  - Generate client SDKs

📘 **See [SWAGGER_IMPLEMENTATION.md](SWAGGER_IMPLEMENTATION.md)** for complete guide!

### Quick Reference

```bash
# Authentication (SignUp → SignIn → Profile → SignOut)
POST   /api/auth/register/              # SignUp - Create account
POST   /api/auth/login/                 # SignIn - Login
GET    /api/auth/me/                    # Profile - Current user
POST   /api/auth/logout/                # SignOut - Logout

# Configuration
GET    /api/config/sub-niches/          # Get 15 trending sub-niches

# Books (Create → Generate → Select Cover → Download)
POST   /api/books/                      # Create book (triggers generation)
GET    /api/books/                      # List user's books
GET    /api/books/{id}/                 # Get book details + 3 covers
POST   /api/books/{id}/select_cover/    # ⚠️ REQUIRED: Select cover
GET    /api/books/{id}/download/        # Download complete PDF
POST   /api/books/{id}/regenerate_covers/  # Generate new covers
POST   /api/books/{id}/regenerate_content/ # Regenerate book content
DELETE /api/books/{id}/                 # Delete book
GET    /api/books/history/              # Get book history
DELETE /api/books/history/              # Clear all books
```

**Postman Collection:** Import `postman_collection.json` for quick testing

**Full Documentation:** See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for:
- Detailed request/response schemas
- Authentication flow
- Status values & workflow
- Error handling
- Code examples (curl, Python, JavaScript)
- Cover styles & niche colors reference

---### Frontend (Planned)

- Vue 3 + TypeScript + Tailwind CSS + DaisyUI

## 🧪 Test It

### Deployment (Planned)

```bash- Backend: Render (free tier)

# Automated test- Frontend: Vercel / Netlify

python test_complete_flow.py- Storage: Cloudflare R2 (free tier, no card)



# Manual test---

curl -X POST http://127.0.0.1:8000/api/auth/register/ \

  -H "Content-Type: application/json" \## 🚦 Current Status

  -d '{"username":"test","email":"test@example.com","password":"test123","password2":"test123"}' \

  -c cookies.txt✅ Backend project initialized  

✅ User, Book, and Cover apps created  

curl -X POST http://127.0.0.1:8000/api/books/ \✅ Groq API integration verified (\`llama-3.1-8b-instant\`)  

  -b cookies.txt \✅ Environment and dependency management ready  

  -d '{"domain":"health","sub_niche":"yoga_beginners","page_length":15}'✅ MIT Licensed  



# Wait 30-60s, then:> 🔜 Next: User authentication, book generation pipeline, and cover designer.

curl http://127.0.0.1:8000/api/books/1/ -b cookies.txt  # Check status

---

curl -X POST http://127.0.0.1:8000/api/books/1/select_cover/ \

  -b cookies.txt \## 🧪 Test Groq Connection

  -d '{"cover_id":1}'

\`\`\`bash

curl http://127.0.0.1:8000/api/books/1/download/ -b cookies.txt -o book.pdfcd backend

```python test_groq.py

# Expected: "✅ Groq API connection successful!"

---\`\`\`



## 🚀 Deploy (Free)---



### Railway.app (Recommended)## 📜 License

```bash

railway loginMIT © 2025 [Badr Ribzat](https://github.com/BadrRibzat)

railway init" > README.md

railway up

railway variables set GROQ_API_KEY=gsk_...
```

### Render.com
1. Connect GitHub repo
2. Add env vars
3. Deploy

### PythonAnywhere
1. Upload code
2. Configure WSGI
3. Set env vars

**Full guide**: See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📂 Project Structure

```
backend/
├── books/
│   ├── models.py              # Book model (status tracking)
│   ├── views.py               # API endpoints
│   ├── serializers.py         # DRF serializers
│   └── services/
│       ├── book_generator.py  # LLM content generation
│       └── pdf_merger.py      # PDF assembly
├── covers/
│   ├── models.py              # Cover model
│   └── services.py            # Cover generation (HTML→PDF)
├── backend/
│   ├── settings.py            # Django config
│   └── utils/mongodb.py       # MongoDB connection
└── media/
    ├── books/                 # Generated PDFs
    └── covers/                # Cover images
```

---

## ⚙️ Configuration

```bash
# .env
SECRET_KEY=your-secret-key
DEBUG=True
GROQ_API_KEY=gsk_...
MONGODB_URI=mongodb+srv://...
MONGODB_DB_NAME=book_generator_db
```

Generate secret key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📊 Performance

| Metric | Time |
|--------|------|
| LLM content generation | 20-40s |
| Cover generation (3) | 10-15s |
| PDF merge | <1s |
| **Total** | **35-65s** |

---

## 💡 Use Cases

- 📚 **Content Creators**: Lead magnets, freebies
- 🎓 **Educators**: Course materials, study guides  
- 💼 **Coaches**: Branded client guides
- 🛍️ **E-commerce**: Digital products to sell
- 🚀 **SaaS**: Launch as subscription product

---

## 📝 Documentation

| File | Description |
|------|-------------|
| **[START_HERE.md](START_HERE.md)** | Quick implementation summary - **Start here!** |
| **[SWAGGER_IMPLEMENTATION.md](SWAGGER_IMPLEMENTATION.md)** | 🆕 **Swagger/ReDoc API docs guide** |
| **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** | Complete REST API reference with examples |
| **[QUICKSTART.md](QUICKSTART.md)** | Step-by-step tutorial |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design & database schema |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment guide |
| **[DIAGRAM.md](DIAGRAM.md)** | Visual architecture diagrams |
| **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** | Full feature checklist |
| **postman_collection.json** | Postman API collection (import & test) |

**🎯 To test the API:** Visit http://127.0.0.1:8000/api/docs/ (Swagger UI)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push and open PR

---

## 🙋 FAQ

**Q: Really no credit card?**  
A: Yes! All services have free tiers.

**Q: Can I customize niches?**  
A: Yes! Edit `books/models.py` and `book_generator.py`.

**Q: Can I use different LLM?**  
A: Yes! Swap Groq for OpenAI/Anthropic in `book_generator.py`.

**Q: Where's the frontend?**  
A: Build with Vue/React - API is framework-agnostic.

---

## 📜 License

MIT License - Use commercially, modify, distribute freely.

---

## 🌟 Support

- **Issues**: https://github.com/BadrRibzat/book-generator/issues
- **Star this repo** if it helped you! ⭐

---

**Made with ❤️ by Badr Ribzat**
