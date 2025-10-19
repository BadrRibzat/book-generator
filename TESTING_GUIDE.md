# Book Generator - Complete Testing Guide

## Prerequisites

Ensure both backend and frontend are running:

```bash
# Terminal 1 - Backend
cd /home/badr/book-generator/backend
source venv/bin/activate
python manage.py runserver

# Terminal 2 - Frontend
cd /home/badr/book-generator/frontend
npm run dev
```

## Test Scenario: Complete Book Generation Flow

### Test 1: Create a Book (No NaN ID)

**Steps:**
1. Navigate to http://localhost:5173
2. Click "Profile" → "Create Book" (or go to `/profile/create`)
3. Fill out the form:
   - Domain: Select "Language & Kids"
   - Sub-Niche: Select "AI-Powered Personalized Learning Stories"
   - Book Length: Select "15 Pages"
4. Click "Generate My Book"

**Expected Results:**
- ✅ No errors in browser console (no `/api/books/NaN/` error)
- ✅ Page redirects to `/books/{id}` where `{id}` is a valid number
- ✅ Backend logs show: `[19/Oct/2025 14:XX:XX] "POST /api/books/ HTTP/1.1" 201 XXX`
- ✅ Response in Network tab shows book object with valid ID:
```json
{
  "id": 1,
  "title": "...",
  "status": "generating",
  ...
}
```

### Test 2: Monitor Generation Progress (Auto-Refresh)

**From Test 1, you should now be on `/books/{id}`**

**Expected Behavior:**
- ✅ Page shows "Book Generation in Progress" card
- ✅ Spinner is spinning next to "Generating Content" status badge
- ✅ Progress bar shows ~50%
- ✅ Message says "6-15 min" (or similar)
- ✅ Every 2 seconds, the page auto-refreshes (you'll see network requests in DevTools)
- ✅ Backend logs show repeated `GET /api/books/{id}/` requests

**To Verify Polling:**
1. Open DevTools → Network tab
2. Filter by "Fetch/XHR"
3. Watch for repeated `/api/books/{id}/` requests appearing every ~2 seconds
4. Each response should have status `generating` initially

### Test 3: Content Generation Completes

**After ~1-2 minutes (depending on implementation):**

**Expected Results:**
- ✅ Status changes to "Content Ready" 
- ✅ "Select a Cover" button appears
- ✅ Polling should continue (no errors)
- ✅ Backend shows status changed to `content_generated`

### Test 4: Select Cover

**From the book details page after content generation:**

**Steps:**
1. Click "Choose Cover Now" button
2. Page navigates to `/books/{id}/covers`
3. Wait for 3 cover options to load
4. Click on one cover to select it
5. Click "Confirm Selection"

**Expected Results:**
- ✅ No "404 Not Found" or "NaN" errors
- ✅ 3 cover images display
- ✅ Selected cover has a blue ring around it
- ✅ After selection, page redirects back to `/books/{id}`
- ✅ Details page now shows:
  - Status: "Ready to Download"
  - Selected cover preview
  - "Download PDF" button

### Test 5: Download Book

**From the book details page after cover selection:**

**Steps:**
1. Click "Download PDF" button

**Expected Results:**
- ✅ PDF file starts downloading
- ✅ File is named something like "[book-title].pdf"
- ✅ Backend logs show: `[19/Oct/2025 14:XX:XX] "GET /api/books/{id}/download/ HTTP/1.1" 200 XXX`

### Test 6: Navigate Back to My Books

**Steps:**
1. Click "My Books" in navigation
2. Go to `/profile/mybooks` or `/profile/books`

**Expected Results:**
- ✅ Book appears in list with "Ready to Download" status
- ✅ No errors in console
- ✅ Can click book to view details again

### Test 7: Delete Book

**From my books list or details page:**

**Steps:**
1. Click "Delete Book" button
2. Confirm deletion

**Expected Results:**
- ✅ Book is removed from list
- ✅ Redirected to my books page
- ✅ Backend logs show: `[19/Oct/2025 14:XX:XX] "DELETE /api/books/{id}/ HTTP/1.1" 204 0`

---

## Browser DevTools - What to Check

### Network Tab Checks:

**After Creating Book:**
```
POST /api/books/ 
Status: 201 ✅
Response: { "id": 1, "status": "generating", ... }
```

**During Generation (polling):**
```
GET /api/books/1/ 
Status: 200 ✅
Response: { "id": 1, "status": "generating", ... }
(repeats every 2 seconds)
```

**After Selecting Cover:**
```
POST /api/books/1/select-cover/
Status: 200 ✅
Response: { "id": 1, "status": "ready", "selected_cover": {...}, ... }
```

**When Downloading:**
```
GET /api/books/1/download/
Status: 200 ✅
Content-Type: application/pdf
```

### Console Tab - Errors to Fix:

**❌ SHOULD NOT SEE:**
- `Failed to load resource: the server responded with a status of 404 (Not Found) /api/books/NaN/`
- `[Vue Router warn]: No match found for location with path "/books"`
- `Access forbidden - user not authenticated` (after login)

**✅ OKAY TO SEE:**
- `"Could not find one or more icon(s)"` - FontAwesome icon warnings (non-critical)

---

## Debugging Common Issues

### Issue: Still Getting NaN in URL

**Solution:**
1. Check browser console for errors
2. Verify backend returned ID in response:
   - Open DevTools → Network → POST /api/books/
   - Check Response tab - ID should be present
3. If ID is missing in response, check backend serializer

### Issue: Polling Not Working

**Check:**
1. Book status should be `generating`
2. Network tab should show repeated GET requests
3. If not polling, check if status is `generating`:
   - If status is different, polling stops automatically

### Issue: Cover Selection Fails

**Check:**
1. Verify covers were generated (book status should be `content_generated`)
2. Check network request for `POST /books/{id}/select-cover/`
3. Ensure cover_id is valid number in request body

### Issue: Download Button Not Appearing

**Check:**
1. Book status should be `ready` (not `cover_pending`)
2. `can_download` field in book object should be `true`
3. `selected_cover` should not be null

---

## Expected Error Messages (That Are OK)

These errors are expected and non-blocking:

```
Could not find one or more icon(s) Object Object
```
(FontAwesome icon loading - visual only, doesn't affect functionality)

---

## Performance Expectations

| Action | Expected Time |
|--------|----------------|
| Create book | < 1 second |
| Generation (15 pages) | 6-15 minutes |
| Cover generation | 2-5 minutes |
| Select cover | < 1 second |
| Download | < 5 seconds |

---

## Success Criteria ✅

All these should work without errors:

- [ ] Create book with valid ID (no NaN)
- [ ] Auto-refresh working during generation
- [ ] Status updates without page redirect
- [ ] Can navigate to cover selection
- [ ] Can select and confirm cover
- [ ] Download button works
- [ ] Can delete books
- [ ] Session persists (no unexpected logouts)
- [ ] No console errors (except icon warnings)

---

## Quick Test Script

If you want to test via API (without UI):

```bash
# 1. Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test5","password":"yourpassword"}' \
  -c cookies.txt

# 2. Create book
curl -X POST http://127.0.0.1:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"domain":"language_kids","sub_niche":"ai_learning_stories","page_length":15}' \
  -b cookies.txt

# 3. Get book details
curl http://127.0.0.1:8000/api/books/1/ -b cookies.txt

# 4. Select cover
curl -X POST http://127.0.0.1:8000/api/books/1/select-cover/ \
  -H "Content-Type: application/json" \
  -d '{"cover_id":1}' \
  -b cookies.txt
```

