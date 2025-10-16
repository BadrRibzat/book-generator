# Quick Start Guide - Book Generator SaaS

## 🚀 Get Started in 5 Minutes

This guide helps you set up and test the complete book generation system locally.

---

## Prerequisites

✅ You already have:
- Python 3.10+ with venv activated
- MongoDB Atlas account (free)
- Groq API key (free)
- All dependencies installed

---

## Step 1: Verify Setup

```bash
cd /home/badr/book-generator/backend
source venv/bin/activate

# Check migrations
python manage.py showmigrations

# Should show:
# books
#  [X] 0001_initial
# covers
#  [X] 0001_initial
```

---

## Step 2: Create Superuser (Optional)

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123 (or your choice)
```

---

## Step 3: Start Development Server

```bash
python manage.py runserver
```

Server running at: http://127.0.0.1:8000

---

## Step 4: Test the API

### Option A: Using curl (Command Line)

#### 1. Register a user
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }' \
  -c cookies.txt \
  | json_pp
```

#### 2. Get available sub-niches
```bash
curl http://127.0.0.1:8000/api/config/sub-niches/ | json_pp
```

#### 3. Create a book
```bash
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "domain": "health",
    "sub_niche": "yoga_beginners",
    "page_length": 15
  }' \
  | json_pp
```

Response:
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

#### 4. Check book status (wait ~30-60 seconds)
```bash
curl http://127.0.0.1:8000/api/books/1/ -b cookies.txt | json_pp
```

Wait until `status` changes to `"cover_pending"` and `covers` array has 3 items.

#### 5. View cover options
The response will include:
```json
{
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
  ]
}
```

#### 6. Select a cover
```bash
curl -X POST http://127.0.0.1:8000/api/books/1/select_cover/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"cover_id": 1}' \
  | json_pp
```

Status should now be `"ready"` and `can_download: true`.

#### 7. Download the book
```bash
curl http://127.0.0.1:8000/api/books/1/download/ \
  -b cookies.txt \
  -o my-yoga-book.pdf
```

Open `my-yoga-book.pdf` - you'll see:
- Professional cover (page 1)
- 15 pages of yoga content
- Proper formatting and typography

---

### Option B: Using Python Requests

Create `test_api.py`:

```python
import requests
import time

BASE_URL = "http://127.0.0.1:8000/api"

# Create session to handle cookies
session = requests.Session()

# 1. Register user
print("1. Registering user...")
response = session.post(f"{BASE_URL}/auth/register/", json={
    "username": "pythontest",
    "email": "python@example.com",
    "password": "testpass123",
    "password2": "testpass123"
})
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# 2. Get sub-niches
print("2. Getting sub-niches...")
response = session.get(f"{BASE_URL}/config/sub-niches/")
niches = response.json()
print(f"Available domains: {[d['label'] for d in niches['domains']]}\n")

# 3. Create book
print("3. Creating book...")
response = session.post(f"{BASE_URL}/books/", json={
    "domain": "food",
    "sub_niche": "vegan_recipes",
    "page_length": 20
})
book = response.json()
book_id = book['id']
print(f"Book created: {book['title']}")
print(f"Status: {book['status']}\n")

# 4. Wait for completion
print("4. Waiting for content generation...")
while True:
    response = session.get(f"{BASE_URL}/books/{book_id}/")
    book = response.json()
    print(f"Status: {book['status']}")
    
    if book['status'] == 'cover_pending':
        print(f"✓ Content generated! {len(book['covers'])} covers available\n")
        break
    elif book['status'] == 'error':
        print(f"✗ Error: {book['error_message']}")
        exit(1)
    
    time.sleep(5)

# 5. List cover options
print("5. Cover options:")
for cover in book['covers']:
    print(f"  - {cover['template_style']} (ID: {cover['id']})")
print()

# 6. Select first cover
cover_id = book['covers'][0]['id']
print(f"6. Selecting cover {cover_id}...")
response = session.post(f"{BASE_URL}/books/{book_id}/select_cover/", json={
    "cover_id": cover_id
})
book = response.json()
print(f"Status: {book['status']}")
print(f"Can download: {book['can_download']}\n")

# 7. Download book
print("7. Downloading book...")
response = session.get(f"{BASE_URL}/books/{book_id}/download/")
if response.status_code == 200:
    filename = f"{book['title']}.pdf"
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"✓ Book saved as: {filename}")
else:
    print(f"✗ Download failed: {response.text}")

print("\n✅ Complete! Check your PDF file.")
```

Run it:
```bash
python test_api.py
```

---

### Option C: Using Browser + REST Client

1. **Install REST Client Extension** (VS Code)
   - Open Extensions
   - Search "REST Client"
   - Install by Huachao Mao

2. **Create `api-test.http`**:

```http
### Variables
@baseUrl = http://127.0.0.1:8000/api
@username = testuser
@password = testpass123

### 1. Register User
POST {{baseUrl}}/auth/register/
Content-Type: application/json

{
  "username": "{{username}}",
  "email": "test@example.com",
  "password": "{{password}}",
  "password2": "{{password}}"
}

### 2. Login
POST {{baseUrl}}/auth/login/
Content-Type: application/json

{
  "username": "{{username}}",
  "password": "{{password}}"
}

### 3. Get Current User
GET {{baseUrl}}/auth/me/

### 4. Get Sub-niches
GET {{baseUrl}}/config/sub-niches/

### 5. Create Book
POST {{baseUrl}}/books/
Content-Type: application/json

{
  "domain": "lifestyle",
  "sub_niche": "minimalism",
  "page_length": 25
}

### 6. Get Book Status (replace {id})
GET {{baseUrl}}/books/1/

### 7. Select Cover (replace {id} and {cover_id})
POST {{baseUrl}}/books/1/select_cover/
Content-Type: application/json

{
  "cover_id": 1
}

### 8. Download Book
GET {{baseUrl}}/books/1/download/

### 9. Get All Books
GET {{baseUrl}}/books/

### 10. Regenerate Covers
POST {{baseUrl}}/books/1/regenerate_covers/
```

3. **Click "Send Request"** above each request

---

## Step 5: Verify Generated Files

```bash
# Check media directory
ls -lh media/books/
ls -lh media/covers/

# Interior PDF (content only)
# book_1_interior.pdf

# Cover images (PNG previews)
# book_1_modern_1234.png
# book_1_bold_5678.png
# book_1_elegant_9012.png

# Cover PDFs (for merging)
# book_1_modern_1234.pdf
# book_1_bold_5678.pdf
# book_1_elegant_9012.pdf

# Final book (cover + interior)
# book_1_final.pdf
```

---

## Step 6: Admin Dashboard (Optional)

```bash
# Visit: http://127.0.0.1:8000/admin
# Login with superuser credentials
```

You can:
- View all books
- Inspect covers
- See user accounts
- Manually trigger actions

---

## Common Issues & Solutions

### Issue: "Book status stuck on 'generating'"

**Solution**: Check terminal for errors. Common causes:
```bash
# 1. Groq API error
# Check .env has correct GROQ_API_KEY

# 2. MongoDB connection failed
# Check MONGODB_URI in .env
# Verify IP whitelist in MongoDB Atlas (use 0.0.0.0/0)

# 3. WeasyPrint missing dependencies
# Install: apt-get install libpango-1.0-0 (Linux)
# Or: brew install pango (macOS)
```

### Issue: "Covers not displaying"

**Solution**:
```bash
# 1. Check media directory exists
mkdir -p media/covers media/books

# 2. Verify MEDIA_URL in settings.py
# Should be: MEDIA_URL = '/media/'

# 3. Check URL routing
# urls.py should include media serving in DEBUG mode
```

### Issue: "Download returns 400 error"

**Solution**: Ensure cover is selected:
```bash
# Check book status
curl http://127.0.0.1:8000/api/books/1/ -b cookies.txt | json_pp

# Must have:
# "status": "ready"
# "can_download": true
# "selected_cover": { ... }
```

---

## Testing All Sub-Niches

Create `test_all_niches.py`:

```python
import requests
import time

session = requests.Session()
BASE_URL = "http://127.0.0.1:8000/api"

# Register once
session.post(f"{BASE_URL}/auth/register/", json={
    "username": "nichetest",
    "email": "niche@example.com",
    "password": "test123",
    "password2": "test123"
})

# Get all sub-niches
response = session.get(f"{BASE_URL}/config/sub-niches/")
niches_data = response.json()

# Test each domain
for domain_item in niches_data['domains']:
    domain = domain_item['value']
    sub_niches = niches_data['sub_niches'][domain]
    
    print(f"\n{'='*60}")
    print(f"Testing Domain: {domain_item['label']}")
    print(f"{'='*60}")
    
    for niche in sub_niches[:1]:  # Test first niche only
        print(f"\nCreating book: {niche['label']}...")
        
        response = session.post(f"{BASE_URL}/books/", json={
            "domain": domain,
            "sub_niche": niche['value'],
            "page_length": 15
        })
        
        if response.status_code == 201:
            book = response.json()
            print(f"✓ Title: {book['title']}")
            print(f"✓ Status: {book['status']}")
        else:
            print(f"✗ Error: {response.text}")

print("\n✅ Niche testing complete!")
```

---

## Performance Benchmarks

Expected generation times (local):

| Component | Time |
|-----------|------|
| Book creation | <1s |
| LLM content generation | 20-40s |
| Interior PDF creation | 2-5s |
| Cover generation (3 covers) | 10-15s |
| PDF merge | <1s |
| **Total** | **35-65s** |

---

## Next Steps

1. ✅ **API Works** → Test all endpoints
2. 🎨 **Build Frontend** → Vue 3 UI (see FRONTEND.md)
3. 🚀 **Deploy** → Follow DEPLOYMENT.md
4. 📊 **Monitor** → Add logging/analytics
5. 💰 **Monetize** → Add premium features

---

## Tips for Development

### Use Django Shell
```bash
python manage.py shell

>>> from books.models import Book
>>> Book.objects.all()
>>> book = Book.objects.first()
>>> book.status
>>> book.covers.all()
```

### View MongoDB Data
```bash
# In Python shell
>>> from backend.utils.mongodb import get_mongodb_db
>>> db = get_mongodb_db()
>>> list(db.book_contents.find())
```

### Reset Everything
```bash
# Delete database
rm db.sqlite3

# Delete media files
rm -rf media/books/* media/covers/*

# Recreate
python manage.py migrate
python manage.py createsuperuser
```

---

## Resources

- **API Docs**: http://127.0.0.1:8000/api/
- **Admin**: http://127.0.0.1:8000/admin/
- **Architecture**: See ARCHITECTURE.md
- **Deployment**: See DEPLOYMENT.md

---

## Support

Having issues? Check:
1. Terminal output for errors
2. `db.sqlite3` exists
3. `.env` file has all variables
4. MongoDB Atlas connection works
5. Groq API key is valid

---

## Success!

🎉 If you can download a complete PDF book with cover, you're ready to:
- Build the frontend
- Deploy to production
- Launch your SaaS!

**Questions?** Open an issue on GitHub.
