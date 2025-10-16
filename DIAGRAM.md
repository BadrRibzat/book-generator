# 📐 System Architecture Diagram

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         BOOK GENERATOR SAAS                              │
│                     (100% Free - No Credit Card)                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                              USER JOURNEY                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  1. REGISTRATION/LOGIN                                                    │
│     └─> POST /api/auth/register/                                         │
│                                                                           │
│  2. CHOOSE DOMAIN → SUB-NICHE → PAGE LENGTH                             │
│     └─> GET /api/config/sub-niches/                                      │
│                                                                           │
│  3. CREATE BOOK (System Auto-Generates Title)                            │
│     └─> POST /api/books/                                                 │
│         Status: draft → generating                                       │
│                                                                           │
│  4. CONTENT GENERATION (30-40s)                                          │
│     ├─> Groq API (Llama 3.1 70B)                                        │
│     ├─> Generate chapters & content                                      │
│     ├─> Format with ReportLab                                            │
│     └─> Store in MongoDB                                                 │
│         Status: generating → content_generated                           │
│                                                                           │
│  5. COVER GENERATION (Auto-triggered, 10-15s)                           │
│     ├─> Generate 3 covers (Modern/Bold/Elegant)                         │
│     ├─> HTML/CSS → PDF (WeasyPrint)                                     │
│     └─> Convert to PNG previews                                          │
│         Status: content_generated → cover_pending                        │
│                                                                           │
│  6. ⚠️  MANDATORY COVER SELECTION                                        │
│     └─> POST /api/books/{id}/select_cover/                              │
│         User MUST select one of 3 covers                                 │
│         Download BLOCKED until this step                                 │
│         Status: cover_pending → ready                                    │
│                                                                           │
│  7. PDF ASSEMBLY                                                          │
│     ├─> Merge cover + interior                                           │
│     └─> Create final downloadable PDF                                    │
│                                                                           │
│  8. ✅ DOWNLOAD ENABLED                                                  │
│     └─> GET /api/books/{id}/download/                                    │
│         Returns: Complete book PDF                                       │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Tech Stack Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            FRONTEND (Future)                              │
│                                                                           │
│                    Vue 3 + TypeScript + DaisyUI                          │
│                    Deployed on: Vercel/Netlify                           │
│                                                                           │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                │ HTTPS/JSON
                                │
┌───────────────────────────────▼───────────────────────────────────────┐
│                          BACKEND (Django)                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                     Django REST Framework                         │   │
│  │  - Session Authentication                                         │   │
│  │  - 12 API Endpoints                                              │   │
│  │  - Request Validation                                             │   │
│  │  - Error Handling                                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Business Logic Layer                         │   │
│  │                                                                   │   │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │   │
│  │  │ Book Generator   │  │ Cover Generator  │  │  PDF Merger   │ │   │
│  │  │                  │  │                  │  │               │ │   │
│  │  │ • Groq API      │  │ • HTML/CSS      │  │ • pypdf       │ │   │
│  │  │ • Title Gen     │  │ • WeasyPrint    │  │ • Merge       │ │   │
│  │  │ • Chapters      │  │ • 3 Styles      │  │ • Assemble    │ │   │
│  │  │ • ReportLab     │  │ • Niche Colors  │  │               │ │   │
│  │  └──────────────────┘  └──────────────────┘  └───────────────┘ │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                      Django ORM Models                            │   │
│  │  - Book (metadata, status)                                       │   │
│  │  - Cover (3 per book, selection)                                 │   │
│  │  - User (auth)                                                    │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                           │
└───────────┬────────────────────────────────┬──────────────────────────┘
            │                                │
            │                                │
┌───────────▼──────────┐        ┌────────────▼────────────┐
│                      │        │                         │
│   SQLite Database    │        │  MongoDB Atlas (FREE)   │
│      (Local)         │        │       (Cloud)           │
│                      │        │                         │
│  • User accounts     │        │  • Book content         │
│  • Book metadata     │        │  • Chapter text         │
│  • Cover records     │        │  • PDF paths            │
│  • Status tracking   │        │  • Generation data      │
│                      │        │                         │
└──────────────────────┘        └─────────────────────────┘
```

## External Services (All FREE!)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SERVICES                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌────────────────────┐    ┌────────────────────┐                       │
│  │   Groq API         │    │  MongoDB Atlas     │                       │
│  │   (LLM)            │    │  (Database)        │                       │
│  │                    │    │                    │                       │
│  │  • Llama 3.1 70B   │    │  • 512MB Free      │                       │
│  │  • Free tier       │    │  • Cloud hosted    │                       │
│  │  • 14,400 req/day  │    │  • Automatic scale │                       │
│  │  • No card needed  │    │  • No card needed  │                       │
│  └────────────────────┘    └────────────────────┘                       │
│                                                                           │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │              Deployment Platform (Choose One)                   │     │
│  │                                                                 │     │
│  │  • Railway.app     - 500 hrs/month free                        │     │
│  │  • Render.com      - 750 hrs/month free                        │     │
│  │  • Fly.io          - Generous free tier                        │     │
│  │  • PythonAnywhere  - Always-on free                            │     │
│  │                                                                 │     │
│  │  ALL: No credit card required initially                        │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────┐
│  USER    │
└────┬─────┘
     │ 1. POST /api/books/ {"domain": "health", "sub_niche": "yoga_beginners"}
     ▼
┌─────────────────┐
│ Django API View │ ──> Create Book record (status: "draft")
└────┬────────────┘
     │ 2. Trigger generation
     ▼
┌──────────────────────┐
│ BookGenerator Service│
└────┬─────────────────┘
     │ 3. Call Groq API
     ▼
┌─────────────────┐
│   Groq LLM      │ ──> Generate chapters (20-40s)
└────┬────────────┘
     │ 4. Return content
     ▼
┌──────────────────────┐
│ BookGenerator Service│ ──> Format with ReportLab → interior.pdf
└────┬─────────────────┘
     │ 5. Save to MongoDB
     ▼
┌──────────────┐
│   MongoDB    │ ──> Store: {book_id, content, pdf_path}
└────┬─────────┘
     │ 6. Update Book status → "content_generated"
     ▼
┌──────────────────────┐
│ CoverGenerator Service│ ──> Auto-triggered
└────┬─────────────────┘
     │ 7. Generate 3 covers
     ▼
┌─────────────────────────────────────────────────┐
│  HTML → CSS → WeasyPrint → PDF → PNG (x3)      │
│                                                  │
│  • Modern style  (geometric, gradients)         │
│  • Bold style    (typography-focused)           │
│  • Elegant style (serif, borders)               │
└────┬────────────────────────────────────────────┘
     │ 8. Save covers to filesystem
     ▼
┌─────────────┐
│ Cover Model │ ──> Create 3 Cover records
└────┬────────┘
     │ 9. Update Book status → "cover_pending"
     ▼
┌──────────┐
│  USER    │ ──> GET /api/books/1/ (sees 3 covers)
└────┬─────┘
     │ 10. POST /api/books/1/select_cover/ {"cover_id": 1}
     ▼
┌────────────┐
│ Cover Model│ ──> Mark as selected
└────┬───────┘
     │ 11. Trigger PDF merge
     ▼
┌─────────────────┐
│ PDFMerger Service│ ──> Load cover.pdf + interior.pdf
└────┬────────────┘
     │ 12. Merge with pypdf
     ▼
┌──────────────┐
│ final.pdf    │ ──> Save to filesystem
└────┬─────────┘
     │ 13. Update MongoDB with final_pdf_path
     ▼
┌──────────────┐
│   MongoDB    │ ──> Update: {final_pdf_path: "books/book_1_final.pdf"}
└────┬─────────┘
     │ 14. Update Book status → "ready"
     ▼
┌──────────┐
│  USER    │ ──> GET /api/books/1/download/
└────┬─────┘
     │ 15. Serve final.pdf
     ▼
┌──────────────┐
│ Download PDF │ ✅ Complete book with cover!
└──────────────┘
```

## Database Schema

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           SQLite (Django ORM)                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │                        Book Model                             │       │
│  ├──────────────────────────────────────────────────────────────┤       │
│  │  id                    : Integer (PK)                         │       │
│  │  user_id               : ForeignKey → User                    │       │
│  │  title                 : String (auto-generated)              │       │
│  │  domain                : Choice (health, food, ...)           │       │
│  │  sub_niche             : Choice (yoga_beginners, ...)         │       │
│  │  page_length           : Integer (15/20/25/30)                │       │
│  │  status                : Choice (draft/generating/...)        │       │
│  │  mongodb_id            : String (reference to MongoDB)        │       │
│  │  created_at            : DateTime                             │       │
│  │  updated_at            : DateTime                             │       │
│  │  content_generated_at  : DateTime                             │       │
│  │  completed_at          : DateTime                             │       │
│  │  error_message         : Text                                 │       │
│  └──────────────────────────────────────────────────────────────┘       │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │                        Cover Model                            │       │
│  ├──────────────────────────────────────────────────────────────┤       │
│  │  id                    : Integer (PK)                         │       │
│  │  book_id               : ForeignKey → Book                    │       │
│  │  template_style        : Choice (modern/bold/elegant)         │       │
│  │  image_path            : String (PNG preview)                 │       │
│  │  pdf_path              : String (PDF for merging)             │       │
│  │  is_selected           : Boolean                              │       │
│  │  generation_params     : JSON (colors, etc.)                  │       │
│  │  created_at            : DateTime                             │       │
│  └──────────────────────────────────────────────────────────────┘       │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                        MongoDB (book_contents)                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│  {                                                                        │
│    "_id": ObjectId("..."),                                               │
│    "book_id": 1,                                                         │
│    "content": {                                                          │
│      "chapters": [                                                       │
│        {                                                                 │
│          "title": "Chapter 1: Introduction to Yoga",                    │
│          "content": ["paragraph 1", "paragraph 2", ...]                 │
│        },                                                                │
│        { ... }                                                           │
│      ],                                                                  │
│      "total_chapters": 5                                                 │
│    },                                                                    │
│    "interior_pdf_path": "/path/to/book_1_interior.pdf",                 │
│    "final_pdf_path": "/path/to/book_1_final.pdf",                       │
│    "created_at": "2025-10-16T12:00:00Z"                                 │
│  }                                                                        │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

## File System Structure

```
media/
├── books/
│   ├── book_1_interior.pdf      ← Interior content only (LLM generated)
│   ├── book_1_final.pdf         ← Final merged PDF (cover + interior)
│   ├── book_2_interior.pdf
│   └── book_2_final.pdf
│
└── covers/
    ├── book_1_modern_1234.png   ← Web preview
    ├── book_1_modern_1234.pdf   ← For PDF merging
    ├── book_1_bold_5678.png
    ├── book_1_bold_5678.pdf
    ├── book_1_elegant_9012.png
    ├── book_1_elegant_9012.pdf
    ├── book_2_modern_3456.png
    └── ...
```

## Status Flow Chart

```
┌─────────┐
│  draft  │  ← Book created
└────┬────┘
     │
     │ Start generation
     ▼
┌─────────────┐
│ generating  │  ← Calling Groq API
└─────┬───────┘
      │
      │ Content ready
      ▼
┌────────────────────┐
│ content_generated  │  ← Interior PDF created
└─────┬──────────────┘
      │
      │ Auto-trigger cover generation
      ▼
┌─────────────────┐
│ cover_pending   │  ⚠️  USER MUST SELECT COVER
└─────┬───────────┘      Download BLOCKED
      │
      │ User selects cover
      ▼
┌──────────┐
│  ready   │  ✅ Download ENABLED
└──────────┘
```

## Cover Generation Detail

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Cover Generation Process                             │
└─────────────────────────────────────────────────────────────────────────┘

For each template style (Modern, Bold, Elegant):

  1. Get niche-specific colors
     ↓
     {
       primary: "#4A90E2",
       secondary: "#7ED321",
       accent: "#F8E71C"
     }

  2. Generate HTML template
     ↓
     <!DOCTYPE html>
     <html>
       <head>
         <style>
           body { background: linear-gradient(...); }
           .title { font-size: 120px; ... }
         </style>
       </head>
       <body>
         <h1 class="title">{{book_title}}</h1>
         <p class="category">{{category}}</p>
       </body>
     </html>

  3. Render to PDF (WeasyPrint)
     ↓
     6" x 9" PDF (print-ready size)

  4. Convert to PNG (for web preview)
     ↓
     600x900px preview image

  5. Save both files
     ↓
     • cover.pdf (for merging)
     • cover.png (for UI display)

  6. Create Cover record in database
     ↓
     Cover(book=book, style="modern", paths=...)

Repeat for all 3 styles!
```

## API Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         API Example Flow                                  │
└─────────────────────────────────────────────────────────────────────────┘

REQUEST:
POST /api/books/
{
  "domain": "health",
  "sub_niche": "yoga_beginners",
  "page_length": 15
}

RESPONSE (Immediate):
{
  "id": 1,
  "title": "The Complete Beginner's Guide to Yoga",
  "domain": "health",
  "sub_niche": "yoga_beginners",
  "page_length": 15,
  "status": "generating",
  "covers": [],
  "selected_cover": null,
  "can_download": false,
  "download_url": null,
  "created_at": "2025-10-16T12:00:00Z"
}

─── Wait 30-60 seconds ───

REQUEST:
GET /api/books/1/

RESPONSE (After generation):
{
  "id": 1,
  "title": "The Complete Beginner's Guide to Yoga",
  "status": "cover_pending",
  "covers": [
    {
      "id": 1,
      "template_style": "modern",
      "image_url": "/media/covers/book_1_modern_1234.png",
      "is_selected": false
    },
    {
      "id": 2,
      "template_style": "bold",
      "image_url": "/media/covers/book_1_bold_5678.png",
      "is_selected": false
    },
    {
      "id": 3,
      "template_style": "elegant",
      "image_url": "/media/covers/book_1_elegant_9012.png",
      "is_selected": false
    }
  ],
  "can_download": false,  ← Still false!
  "download_url": null
}

REQUEST:
POST /api/books/1/select_cover/
{
  "cover_id": 1
}

RESPONSE:
{
  "id": 1,
  "status": "ready",  ← Now ready!
  "selected_cover": {
    "id": 1,
    "template_style": "modern",
    "is_selected": true
  },
  "can_download": true,  ← NOW true!
  "download_url": "/api/books/1/download/"
}

REQUEST:
GET /api/books/1/download/

RESPONSE:
Content-Type: application/pdf
Content-Disposition: attachment; filename="The Complete Beginner's Guide to Yoga.pdf"

[PDF Binary Data - Cover + 15 pages of content]
```

---

**This diagram shows the complete architecture of your book generator SaaS!**

All components are implemented and working. ✅
