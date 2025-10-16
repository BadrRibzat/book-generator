# 📡 REST API Documentation

## Base URL

```
Development: http://127.0.0.1:8000/api
Production:  https://your-domain.com/api
```

---

## 🔐 Authentication

The API uses **session-based authentication** with Django sessions. After login, a session cookie is set and must be included in subsequent requests.

### CSRF Protection

For POST/PUT/DELETE requests, include the CSRF token:
- Cookie: `csrftoken`
- Header: `X-CSRFToken`

Django REST Framework handles this automatically when using the browsable API.

---

## 📋 API Endpoints Overview

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| POST | `/auth/register/` | No | Register new user |
| POST | `/auth/login/` | No | Login user |
| POST | `/auth/logout/` | Yes | Logout user |
| GET | `/auth/me/` | Yes | Get current user |
| GET | `/config/sub-niches/` | No | Get available options |
| POST | `/books/` | Yes | Create book |
| GET | `/books/` | Yes | List user's books |
| GET | `/books/{id}/` | Yes | Get book details |
| POST | `/books/{id}/select_cover/` | Yes | Select cover |
| GET | `/books/{id}/download/` | Yes | Download PDF |
| POST | `/books/{id}/regenerate_covers/` | Yes | Regenerate covers |
| POST | `/books/{id}/regenerate_content/` | Yes | Regenerate content |
| GET | `/books/history/` | Yes | Get book history |
| DELETE | `/books/history/` | Yes | Clear all books |
| PUT | `/books/{id}/` | Yes | Update book (not implemented) |
| DELETE | `/books/{id}/` | Yes | Delete book |

---

## 🔑 Authentication Endpoints

### Register User

Create a new user account.

**Endpoint:** `POST /api/auth/register/`

**Request Body:**
```json
{
  "username": "string",      // Required, 3-150 chars, unique
  "email": "string",         // Required, valid email
  "password": "string",      // Required, min 8 chars
  "password2": "string"      // Required, must match password
}
```

**Success Response: 201 Created**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "message": "Registration successful"
}
```

**Error Response: 400 Bad Request**
```json
{
  "username": ["A user with that username already exists."],
  "password": ["Passwords must match"],
  "email": ["Enter a valid email address."]
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "password2": "securepass123"
  }' \
  -c cookies.txt
```

---

### Login User

Authenticate and create a session.

**Endpoint:** `POST /api/auth/login/`

**Request Body:**
```json
{
  "username": "string",      // Required
  "password": "string"       // Required
}
```

**Success Response: 200 OK**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "message": "Login successful"
}
```

**Error Response: 400 Bad Request**
```json
{
  "error": "Username and password required"
}
```

**Error Response: 401 Unauthorized**
```json
{
  "error": "Invalid credentials"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }' \
  -c cookies.txt
```

---

### Logout User

End the current session.

**Endpoint:** `POST /api/auth/logout/`

**Authentication:** Required

**Request Body:** None

**Success Response: 200 OK**
```json
{
  "message": "Logout successful"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/logout/ \
  -b cookies.txt
```

---

### Get Current User

Get authenticated user information.

**Endpoint:** `GET /api/auth/me/`

**Authentication:** Required

**Success Response: 200 OK**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com"
}
```

**Error Response: 401 Unauthorized**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/auth/me/ \
  -b cookies.txt
```

---

## ⚙️ Configuration Endpoints

### Get Sub-Niches

Get available domains, sub-niches, and page lengths.

**Endpoint:** `GET /api/config/sub-niches/`

**Authentication:** Not required

**Success Response: 200 OK**
```json
{
  "domains": [
    {
      "value": "health",
      "label": "Health & Wellness"
    },
    {
      "value": "food",
      "label": "Food & Nutrition"
    },
    {
      "value": "personal_dev",
      "label": "Personal Development"
    },
    {
      "value": "hobbies",
      "label": "Hobbies & Crafts"
    },
    {
      "value": "lifestyle",
      "label": "Lifestyle"
    }
  ],
  "sub_niches": {
    "health": [
      {
        "value": "yoga_beginners",
        "label": "Yoga for Beginners"
      },
      {
        "value": "home_workouts",
        "label": "Home Workouts"
      },
      {
        "value": "mental_wellness",
        "label": "Mental Wellness"
      }
    ],
    "food": [
      {
        "value": "vegan_recipes",
        "label": "Vegan Recipes"
      },
      {
        "value": "meal_prep",
        "label": "Meal Prep Guide"
      },
      {
        "value": "smoothie_recipes",
        "label": "Smoothie Recipes"
      }
    ],
    "personal_dev": [
      {
        "value": "productivity",
        "label": "Productivity Hacks"
      },
      {
        "value": "morning_routines",
        "label": "Morning Routines"
      },
      {
        "value": "goal_setting",
        "label": "Goal Setting"
      }
    ],
    "hobbies": [
      {
        "value": "gardening",
        "label": "Home Gardening"
      },
      {
        "value": "photography",
        "label": "Photography Basics"
      },
      {
        "value": "diy_crafts",
        "label": "DIY Crafts"
      }
    ],
    "lifestyle": [
      {
        "value": "minimalism",
        "label": "Minimalist Living"
      },
      {
        "value": "sustainable_living",
        "label": "Sustainable Living"
      },
      {
        "value": "travel_hacks",
        "label": "Travel Hacks"
      }
    ]
  },
  "page_lengths": [15, 20, 25, 30]
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/config/sub-niches/
```

---

## 📚 Book Endpoints

### Create Book

Create a new book and trigger content generation.

**Endpoint:** `POST /api/books/`

**Authentication:** Required

**Request Body:**
```json
{
  "domain": "string",         // Required, one of: health, food, personal_dev, hobbies, lifestyle
  "sub_niche": "string",      // Required, must match domain
  "page_length": integer      // Required, one of: 15, 20, 25, 30
}
```

**Success Response: 201 Created**
```json
{
  "id": 1,
  "title": "The Complete Beginner's Guide to Yoga",
  "domain": "health",
  "sub_niche": "yoga_beginners",
  "page_length": 15,
  "status": "generating",
  "created_at": "2025-10-16T12:00:00Z",
  "updated_at": "2025-10-16T12:00:00Z",
  "completed_at": null,
  "covers": [],
  "selected_cover": null,
  "can_download": false,
  "download_url": null,
  "error_message": null
}
```

**Error Response: 400 Bad Request**
```json
{
  "sub_niche": ["Sub-niche 'vegan_recipes' not valid for domain 'health'"]
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "domain": "health",
    "sub_niche": "yoga_beginners",
    "page_length": 20
  }'
```

**Notes:**
- Title is auto-generated based on sub-niche
- Content generation starts immediately (async)
- Status will change: `draft` → `generating` → `content_generated` → `cover_pending`
- Poll `GET /api/books/{id}/` to check status

---

### List Books

Get all books for the authenticated user.

**Endpoint:** `GET /api/books/`

**Authentication:** Required

**Query Parameters:**
- None (always returns current user's books)

**Success Response: 200 OK**
```json
[
  {
    "id": 1,
    "title": "The Complete Beginner's Guide to Yoga",
    "domain": "health",
    "sub_niche": "yoga_beginners",
    "page_length": 15,
    "status": "ready",
    "created_at": "2025-10-16T12:00:00Z",
    "updated_at": "2025-10-16T12:01:00Z",
    "completed_at": "2025-10-16T12:01:00Z",
    "covers": [
      {
        "id": 1,
        "template_style": "modern",
        "image_path": "covers/book_1_modern_1234.png",
        "image_url": "/media/covers/book_1_modern_1234.png",
        "is_selected": true,
        "created_at": "2025-10-16T12:00:45Z",
        "generation_params": {
          "colors": {
            "primary": "#4A90E2",
            "secondary": "#7ED321",
            "accent": "#F8E71C"
          },
          "template": "modern"
        }
      },
      {
        "id": 2,
        "template_style": "bold",
        "image_path": "covers/book_1_bold_5678.png",
        "image_url": "/media/covers/book_1_bold_5678.png",
        "is_selected": false,
        "created_at": "2025-10-16T12:00:45Z",
        "generation_params": {
          "colors": {
            "primary": "#4A90E2",
            "secondary": "#7ED321",
            "accent": "#F8E71C"
          },
          "template": "bold"
        }
      },
      {
        "id": 3,
        "template_style": "elegant",
        "image_path": "covers/book_1_elegant_9012.png",
        "image_url": "/media/covers/book_1_elegant_9012.png",
        "is_selected": false,
        "created_at": "2025-10-16T12:00:45Z",
        "generation_params": {
          "colors": {
            "primary": "#4A90E2",
            "secondary": "#7ED321",
            "accent": "#F8E71C"
          },
          "template": "elegant"
        }
      }
    ],
    "selected_cover": {
      "id": 1,
      "template_style": "modern",
      "image_path": "covers/book_1_modern_1234.png",
      "image_url": "/media/covers/book_1_modern_1234.png",
      "is_selected": true,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {
        "colors": {
          "primary": "#4A90E2",
          "secondary": "#7ED321",
          "accent": "#F8E71C"
        },
        "template": "modern"
      }
    },
    "can_download": true,
    "download_url": "/api/books/1/download/",
    "error_message": null
  },
  {
    "id": 2,
    "title": "Plant-Based Delights: 25 Vegan Recipes",
    "domain": "food",
    "sub_niche": "vegan_recipes",
    "page_length": 25,
    "status": "cover_pending",
    "created_at": "2025-10-16T13:00:00Z",
    "updated_at": "2025-10-16T13:00:45Z",
    "completed_at": null,
    "covers": [
      {
        "id": 4,
        "template_style": "modern",
        "image_path": "covers/book_2_modern_3456.png",
        "image_url": "/media/covers/book_2_modern_3456.png",
        "is_selected": false,
        "created_at": "2025-10-16T13:00:45Z",
        "generation_params": {
          "colors": {
            "primary": "#27AE60",
            "secondary": "#F39C12",
            "accent": "#E74C3C"
          },
          "template": "modern"
        }
      },
      {
        "id": 5,
        "template_style": "bold",
        "image_path": "covers/book_2_bold_7890.png",
        "image_url": "/media/covers/book_2_bold_7890.png",
        "is_selected": false,
        "created_at": "2025-10-16T13:00:45Z",
        "generation_params": {
          "colors": {
            "primary": "#27AE60",
            "secondary": "#F39C12",
            "accent": "#E74C3C"
          },
          "template": "bold"
        }
      },
      {
        "id": 6,
        "template_style": "elegant",
        "image_path": "covers/book_2_elegant_1234.png",
        "image_url": "/media/covers/book_2_elegant_1234.png",
        "is_selected": false,
        "created_at": "2025-10-16T13:00:45Z",
        "generation_params": {
          "colors": {
            "primary": "#27AE60",
            "secondary": "#F39C12",
            "accent": "#E74C3C"
          },
          "template": "elegant"
        }
      }
    ],
    "selected_cover": null,
    "can_download": false,
    "download_url": null,
    "error_message": null
  }
]
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/books/ \
  -b cookies.txt
```

---

### Get Book Details

Get detailed information about a specific book.

**Endpoint:** `GET /api/books/{id}/`

**Authentication:** Required

**Path Parameters:**
- `id` (integer): Book ID

**Success Response: 200 OK**
```json
{
  "id": 1,
  "title": "The Complete Beginner's Guide to Yoga",
  "domain": "health",
  "sub_niche": "yoga_beginners",
  "page_length": 15,
  "status": "cover_pending",
  "created_at": "2025-10-16T12:00:00Z",
  "updated_at": "2025-10-16T12:00:45Z",
  "completed_at": null,
  "covers": [
    {
      "id": 1,
      "template_style": "modern",
      "image_path": "covers/book_1_modern_1234.png",
      "image_url": "/media/covers/book_1_modern_1234.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {
        "colors": {
          "primary": "#4A90E2",
          "secondary": "#7ED321",
          "accent": "#F8E71C"
        },
        "template": "modern"
      }
    },
    {
      "id": 2,
      "template_style": "bold",
      "image_path": "covers/book_1_bold_5678.png",
      "image_url": "/media/covers/book_1_bold_5678.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {
        "colors": {
          "primary": "#4A90E2",
          "secondary": "#7ED321",
          "accent": "#F8E71C"
        },
        "template": "bold"
      }
    },
    {
      "id": 3,
      "template_style": "elegant",
      "image_path": "covers/book_1_elegant_9012.png",
      "image_url": "/media/covers/book_1_elegant_9012.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {
        "colors": {
          "primary": "#4A90E2",
          "secondary": "#7ED321",
          "accent": "#F8E71C"
        },
        "template": "elegant"
      }
    }
  ],
  "selected_cover": null,
  "can_download": false,
  "download_url": null,
  "error_message": null
}
```

**Error Response: 404 Not Found**
```json
{
  "detail": "Not found."
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/books/1/ \
  -b cookies.txt
```

**Notes:**
- Use this endpoint to poll for status changes
- When status is `cover_pending`, covers array will have 3 items
- `can_download` is `false` until cover is selected

---

### Select Cover

Select one of the three generated covers (required before download).

**Endpoint:** `POST /api/books/{id}/select_cover/`

**Authentication:** Required

**Path Parameters:**
- `id` (integer): Book ID

**Request Body:**
```json
{
  "cover_id": integer      // Required, must be one of the book's cover IDs
}
```

**Success Response: 200 OK**
```json
{
  "id": 1,
  "title": "The Complete Beginner's Guide to Yoga",
  "domain": "health",
  "sub_niche": "yoga_beginners",
  "page_length": 15,
  "status": "ready",
  "created_at": "2025-10-16T12:00:00Z",
  "updated_at": "2025-10-16T12:01:00Z",
  "completed_at": "2025-10-16T12:01:00Z",
  "covers": [
    {
      "id": 1,
      "template_style": "modern",
      "image_path": "covers/book_1_modern_1234.png",
      "image_url": "/media/covers/book_1_modern_1234.png",
      "is_selected": true,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {
        "colors": {
          "primary": "#4A90E2",
          "secondary": "#7ED321",
          "accent": "#F8E71C"
        },
        "template": "modern"
      }
    },
    {
      "id": 2,
      "template_style": "bold",
      "image_path": "covers/book_1_bold_5678.png",
      "image_url": "/media/covers/book_1_bold_5678.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {}
    },
    {
      "id": 3,
      "template_style": "elegant",
      "image_path": "covers/book_1_elegant_9012.png",
      "image_url": "/media/covers/book_1_elegant_9012.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:00:45Z",
      "generation_params": {}
    }
  ],
  "selected_cover": {
    "id": 1,
    "template_style": "modern",
    "image_path": "covers/book_1_modern_1234.png",
    "image_url": "/media/covers/book_1_modern_1234.png",
    "is_selected": true,
    "created_at": "2025-10-16T12:00:45Z",
    "generation_params": {
      "colors": {
        "primary": "#4A90E2",
        "secondary": "#7ED321",
        "accent": "#F8E71C"
      },
      "template": "modern"
    }
  },
  "can_download": true,
  "download_url": "/api/books/1/download/",
  "error_message": null
}
```

**Error Response: 400 Bad Request**
```json
{
  "error": "cover_id is required"
}
```

```json
{
  "error": "Content must be generated first"
}
```

```json
{
  "error": "Invalid cover_id or cover not found"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/books/1/select_cover/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"cover_id": 1}'
```

**Notes:**
- This action triggers PDF merging (cover + interior)
- Status changes from `cover_pending` to `ready`
- `can_download` becomes `true`
- Only one cover can be selected per book
- Selecting a new cover deselects the previous one

---

### Download Book

Download the final PDF (cover + interior).

**Endpoint:** `GET /api/books/{id}/download/`

**Authentication:** Required

**Path Parameters:**
- `id` (integer): Book ID

**Success Response: 200 OK**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="The Complete Beginner's Guide to Yoga.pdf"

[PDF Binary Data]
```

**Error Response: 400 Bad Request**
```json
{
  "error": "Book not ready. Please select a cover first."
}
```

**Error Response: 404 Not Found**
```json
{
  "error": "Final PDF not found"
}
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/books/1/download/ \
  -b cookies.txt \
  -o my-book.pdf
```

**Notes:**
- Only works when `status` is `ready` and `can_download` is `true`
- Returns actual PDF file (not JSON)
- Filename is based on book title
- PDF includes cover (page 1) + interior pages

---

### Regenerate Covers

Generate 3 new cover options for a book.

**Endpoint:** `POST /api/books/{id}/regenerate_covers/`

**Authentication:** Required

**Path Parameters:**
- `id` (integer): Book ID

**Request Body:** None

**Success Response: 200 OK**
```json
{
  "id": 1,
  "title": "The Complete Beginner's Guide to Yoga",
  "status": "cover_pending",
  "covers": [
    {
      "id": 4,
      "template_style": "modern",
      "image_path": "covers/book_1_modern_5678.png",
      "image_url": "/media/covers/book_1_modern_5678.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:05:00Z",
      "generation_params": {}
    },
    {
      "id": 5,
      "template_style": "bold",
      "image_path": "covers/book_1_bold_9012.png",
      "image_url": "/media/covers/book_1_bold_9012.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:05:00Z",
      "generation_params": {}
    },
    {
      "id": 6,
      "template_style": "elegant",
      "image_path": "covers/book_1_elegant_3456.png",
      "image_url": "/media/covers/book_1_elegant_3456.png",
      "is_selected": false,
      "created_at": "2025-10-16T12:05:00Z",
      "generation_params": {}
    }
  ],
  "selected_cover": null,
  "can_download": false,
  "download_url": null
}
```

**Error Response: 400 Bad Request**
```json
{
  "error": "Content must be generated first"
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/books/1/regenerate_covers/ \
  -b cookies.txt
```

**Notes:**
- Deletes all previous covers
- Generates 3 brand new covers with same niche colors
- Status changes to `cover_pending` (if it was `ready`)
- User must select cover again

---

### Regenerate Content

Regenerate the entire book content (keeps same configuration).

**Endpoint:** `POST /api/books/{id}/regenerate_content/`

**Authentication:** Required

**Path Parameters:**
- `id` (integer): Book ID

**Request Body:** None

**Success Response: 200 OK**
```json
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
  "download_url": null
}
```

**Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/books/1/regenerate_content/ \
  -b cookies.txt
```

**Notes:**
- Deletes all covers
- Resets status to `draft` then `generating`
- Generates new content from LLM (may be different)
- New covers will be generated after content completes

---

### Get Book History

Get all books for the authenticated user (same as List Books).

**Endpoint:** `GET /api/books/history/`

**Authentication:** Required

**Success Response: 200 OK**
```json
[
  {
    "id": 1,
    "title": "The Complete Beginner's Guide to Yoga",
    "domain": "health",
    "sub_niche": "yoga_beginners",
    "page_length": 15,
    "status": "ready",
    "created_at": "2025-10-16T12:00:00Z",
    "covers": [...],
    "selected_cover": {...},
    "can_download": true,
    "download_url": "/api/books/1/download/"
  },
  ...
]
```

**Example:**
```bash
curl http://127.0.0.1:8000/api/books/history/ \
  -b cookies.txt
```

**Notes:**
- Identical to `GET /api/books/`
- Provided for semantic clarity

---

### Clear History

Delete all books for the authenticated user.

**Endpoint:** `DELETE /api/books/history/`

**Authentication:** Required

**Request Body:** None

**Success Response: 204 No Content**

**Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/books/history/ \
  -b cookies.txt
```

**Notes:**
- Deletes all books and associated covers
- PDFs remain in filesystem (can be cleaned separately)
- Cannot be undone

---

### Delete Single Book

Delete a specific book.

**Endpoint:** `DELETE /api/books/{id}/`

**Authentication:** Required

**Path Parameters:**
- `id` (integer): Book ID

**Success Response: 204 No Content**

**Error Response: 404 Not Found**
```json
{
  "detail": "Not found."
}
```

**Example:**
```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1/ \
  -b cookies.txt
```

---

## 📊 Status Values

Books have the following status values:

| Status | Description | User Action |
|--------|-------------|-------------|
| `draft` | Book created, not yet started | None - automatic |
| `generating` | LLM is generating content | Wait - poll for updates |
| `content_generated` | Content ready, covers being generated | Wait - automatic |
| `cover_pending` | 3 covers ready, user must select | **SELECT A COVER** |
| `ready` | Cover selected, PDF assembled | Download book |
| `error` | Generation failed | Check `error_message` |

---

## 🎨 Cover Styles

Each book generates 3 covers with different styles:

### Modern
- Minimalist design
- Geometric shapes
- Gradient backgrounds
- Clean typography
- Example color: Blue/Green gradients

### Bold
- Typography-focused
- High contrast
- Large text
- Solid colors
- Example: Dark background, bright accents

### Elegant
- Professional appearance
- Serif fonts
- Border frames
- Classic layout
- Example: White background, thin borders

---

## 🌈 Niche-Specific Colors

Each sub-niche has custom color schemes:

| Sub-Niche | Primary | Secondary | Accent |
|-----------|---------|-----------|--------|
| yoga_beginners | #4A90E2 | #7ED321 | #F8E71C |
| home_workouts | #E74C3C | #F39C12 | #34495E |
| mental_wellness | #9B59B6 | #3498DB | #ECF0F1 |
| vegan_recipes | #27AE60 | #F39C12 | #E74C3C |
| meal_prep | #E67E22 | #3498DB | #2ECC71 |
| smoothie_recipes | #E91E63 | #9C27B0 | #FF5722 |
| productivity | #2C3E50 | #3498DB | #F39C12 |
| morning_routines | #FF9800 | #FFC107 | #FF5722 |
| goal_setting | #673AB7 | #9C27B0 | #E91E63 |
| gardening | #4CAF50 | #8BC34A | #CDDC39 |
| photography | #212121 | #757575 | #FF5722 |
| diy_crafts | #FF6F61 | #FFA726 | #AB47BC |
| minimalism | #263238 | #90A4AE | #ECEFF1 |
| sustainable_living | #388E3C | #689F38 | #AFB42B |
| travel_hacks | #0277BD | #0288D1 | #03A9F4 |

---

## ⚠️ Error Responses

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 204 | No Content | Successful deletion |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | Not authenticated |
| 403 | Forbidden | Not authorized |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "error": "Human-readable error message"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message for this field"],
  "another_field": ["Another error message"]
}
```

---

## 🔄 Complete Workflow Example

### 1. Register & Login

```bash
# Register
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bookfan",
    "email": "fan@example.com",
    "password": "mypass123",
    "password2": "mypass123"
  }' \
  -c cookies.txt

# Response: {"user": {...}, "message": "Registration successful"}
```

### 2. Get Available Options

```bash
curl http://127.0.0.1:8000/api/config/sub-niches/

# Response: {"domains": [...], "sub_niches": {...}, "page_lengths": [...]}
```

### 3. Create Book

```bash
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "domain": "personal_dev",
    "sub_niche": "productivity",
    "page_length": 20
  }'

# Response: {"id": 1, "title": "...", "status": "generating", ...}
```

### 4. Poll for Status

```bash
# Wait 30-60 seconds, then check status
curl http://127.0.0.1:8000/api/books/1/ -b cookies.txt

# Keep checking until status is "cover_pending"
# Response: {"id": 1, "status": "cover_pending", "covers": [{...}, {...}, {...}], ...}
```

### 5. Select Cover

```bash
curl -X POST http://127.0.0.1:8000/api/books/1/select_cover/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"cover_id": 1}'

# Response: {"id": 1, "status": "ready", "can_download": true, ...}
```

### 6. Download Book

```bash
curl http://127.0.0.1:8000/api/books/1/download/ \
  -b cookies.txt \
  -o productivity-book.pdf

# Response: PDF file downloaded
```

### 7. View History

```bash
curl http://127.0.0.1:8000/api/books/history/ \
  -b cookies.txt

# Response: [{"id": 1, "title": "...", "status": "ready", ...}, ...]
```

---

## 🐍 Python Client Example

```python
import requests
import time

BASE_URL = "http://127.0.0.1:8000/api"
session = requests.Session()

# 1. Register
response = session.post(f"{BASE_URL}/auth/register/", json={
    "username": "pythonclient",
    "email": "python@example.com",
    "password": "secure123",
    "password2": "secure123"
})
print(f"Registered: {response.json()}")

# 2. Create book
response = session.post(f"{BASE_URL}/books/", json={
    "domain": "lifestyle",
    "sub_niche": "minimalism",
    "page_length": 25
})
book = response.json()
book_id = book['id']
print(f"Book created: {book['title']}")

# 3. Wait for covers
while True:
    response = session.get(f"{BASE_URL}/books/{book_id}/")
    book = response.json()
    print(f"Status: {book['status']}")
    
    if book['status'] == 'cover_pending':
        print(f"Covers ready: {len(book['covers'])}")
        break
    elif book['status'] == 'error':
        print(f"Error: {book['error_message']}")
        exit(1)
    
    time.sleep(5)

# 4. Select first cover
cover_id = book['covers'][0]['id']
response = session.post(f"{BASE_URL}/books/{book_id}/select_cover/", json={
    "cover_id": cover_id
})
book = response.json()
print(f"Cover selected. Status: {book['status']}")

# 5. Download
response = session.get(f"{BASE_URL}/books/{book_id}/download/")
with open("my-book.pdf", "wb") as f:
    f.write(response.content)
print("Book downloaded!")
```

---

## 🌐 JavaScript/Fetch Example

```javascript
const BASE_URL = 'http://127.0.0.1:8000/api';

async function createAndDownloadBook() {
  // 1. Register
  let response = await fetch(`${BASE_URL}/auth/register/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      username: 'jsclient',
      email: 'js@example.com',
      password: 'pass123',
      password2: 'pass123'
    })
  });
  console.log('Registered:', await response.json());

  // 2. Create book
  response = await fetch(`${BASE_URL}/books/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      domain: 'health',
      sub_niche: 'mental_wellness',
      page_length: 15
    })
  });
  const book = await response.json();
  console.log('Book created:', book.title);

  // 3. Wait for covers
  while (true) {
    response = await fetch(`${BASE_URL}/books/${book.id}/`, {
      credentials: 'include'
    });
    const bookData = await response.json();
    console.log('Status:', bookData.status);

    if (bookData.status === 'cover_pending') {
      console.log('Covers ready:', bookData.covers.length);
      
      // 4. Select cover
      const coverId = bookData.covers[0].id;
      response = await fetch(`${BASE_URL}/books/${book.id}/select_cover/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ cover_id: coverId })
      });
      console.log('Cover selected');
      
      // 5. Download
      response = await fetch(`${BASE_URL}/books/${book.id}/download/`, {
        credentials: 'include'
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'book.pdf';
      a.click();
      console.log('Book downloaded!');
      
      break;
    } else if (bookData.status === 'error') {
      console.error('Error:', bookData.error_message);
      break;
    }

    await new Promise(resolve => setTimeout(resolve, 5000));
  }
}

createAndDownloadBook();
```

---

## 📝 Notes & Best Practices

### Polling
- Poll `GET /api/books/{id}/` every 3-5 seconds during generation
- Stop polling once status is `cover_pending` or `error`
- Show progress indicator to users

### Error Handling
- Always check `status` field before attempting actions
- Display `error_message` field to users if status is `error`
- Validate input on frontend before API calls

### Performance
- Generation takes 30-60 seconds total
- LLM calls: 20-40s
- Cover generation: 10-15s
- PDF merge: <1s

### File Storage
- Cover images: `/media/covers/book_{id}_{style}_{random}.png`
- Cover PDFs: `/media/covers/book_{id}_{style}_{random}.pdf`
- Interior PDFs: `/media/books/book_{id}_interior.pdf`
- Final PDFs: `/media/books/book_{id}_final.pdf`

### Rate Limiting
- Not implemented yet
- Consider adding for production
- Groq free tier: 14,400 requests/day

---

## 🔐 Security Considerations

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS only
- [ ] Enable `SECURE_SSL_REDIRECT`
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Set `CSRF_COOKIE_SECURE=True`
- [ ] Configure CORS for frontend domain
- [ ] Add rate limiting
- [ ] Implement request timeouts
- [ ] Sanitize user inputs
- [ ] Monitor API usage

---

## 📞 Support

**Questions about the API?**
- Check this documentation first
- Review code examples
- Test with curl/Postman
- Open GitHub issue

**Base URL:** `http://127.0.0.1:8000/api` (development)

**API Version:** 1.0

**Last Updated:** October 16, 2025
