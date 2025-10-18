# Route Structure Overview

## Frontend Routes (Vue Router)

### Public Routes (No Authentication Required)
```
/                       → Home.vue
/features              → Features.vue  
/about                 → About.vue
/pricing               → Pricing.vue
/please-signin         → PleaseSignIn.vue (redirect page for unauthenticated users)
```

### Authentication Routes (Guest Only - redirect to /profile if authenticated)
```
/auth/signup           → Auth/SignUp.vue
/auth/signin           → Auth/SignIn.vue
```

### Profile Routes (Authentication Required - redirect to /please-signin if not authenticated)
```
/profile               → Profile.vue (user profile/dashboard)
/profile/books         → Books/List.vue (browse/search books)
/profile/create        → Books/Create.vue (create new book)
/profile/mybooks       → Books/List.vue (user's book library)
```

### Book Detail Routes (Authentication Required)
```
/books/:id             → Books/Details.vue (book details with props)
/books/:id/covers      → Books/SelectCover.vue (select cover for book)
```

## Backend API Endpoints

### Authentication
```
POST   /api/auth/register/     Register new user (SignUp)
POST   /api/auth/login/        Login user (SignIn)
POST   /api/auth/logout/       Logout user (SignOut)
GET    /api/auth/me/           Get current user info (requires auth)
```

### Configuration
```
GET    /api/config/sub-niches/  Get available domains and sub-niches
```

### Books (All require authentication)
```
GET    /api/books/                    List user's books
POST   /api/books/                    Create new book
GET    /api/books/:id/                Get book details
PUT    /api/books/:id/                Update book
DELETE /api/books/:id/                Delete book
POST   /api/books/:id/select_cover/   Select a cover for the book
POST   /api/books/:id/regenerate_covers/  Regenerate cover options
GET    /api/books/:id/download/       Download final PDF
POST   /api/books/:id/regenerate_content/  Regenerate book content
GET    /api/books/history/            Get user's book history
DELETE /api/books/clear_history/     Delete all user's books
```

## Navigation Flow

### User Journey (Unauthenticated)
```
1. Visit homepage (/)
2. Click "Get Started" or "Sign In"
3. Choose:
   a. /auth/signup → Create account → Redirect to /auth/signin
   b. /auth/signin → Enter credentials → Redirect to /profile
```

### User Journey (Authenticated)
```
1. Land on /profile (dashboard)
2. Navigation options:
   - "My Books" button → /profile/mybooks (view your library)
   - "Create Book" button → /profile/create (start new book)
   - "Profile" button → /profile (back to dashboard)
3. Click on a book → /books/:id (book details)
4. Select cover → /books/:id/covers (choose from 3 options)
5. Download → final PDF download
```

### Protected Route Behavior
```
If user tries to access /profile/* without authentication:
→ Redirects to /please-signin
→ PleaseSignIn page shows friendly message with link to /auth/signin

If authenticated user tries to access /auth/signup or /auth/signin:
→ Redirects to /profile (already signed in)
```

## Component Relationships

### Layout.vue (Navigation Bar)
```
When Authenticated:
- "My Books" link → /profile/mybooks
- "Profile" button → /profile

When Not Authenticated:
- "Sign In" link → /auth/signin
- "Get Started" button → /auth/signup
```

### Auth Flow
```
SignUp.vue:
  - Form submission → POST /api/auth/register/
  - Success → router.push('/auth/signin')

SignIn.vue:
  - Form submission → POST /api/auth/login/
  - Success → Check session → router.replace('/profile')
  - Supports redirect query param: /auth/signin?redirect=/profile/create
```

### Profile Pages
```
Profile.vue:
  - Shows user info from auth store
  - Links to /profile/create and /profile/mybooks

Books/Create.vue:
  - Form to create new book
  - POST /api/books/
  - Success → router.push(`/books/${bookId}`)

Books/List.vue:
  - Used for both /profile/books and /profile/mybooks
  - GET /api/books/
  - Click book → router.push(`/books/${book.id}`)

Books/Details.vue:
  - Shows book details and status
  - Links to /books/:id/covers when covers ready
  - Download button when book ready

Books/SelectCover.vue:
  - Shows 3 cover options
  - POST /api/books/:id/select_cover/
  - Success → router.push(`/books/${book.id}`)
```

## Session Management

### How Authentication Works
```
1. User submits login form
2. POST /api/auth/login/ with username & password
3. Backend creates session, returns sessionid cookie
4. Frontend stores cookie (withCredentials: true)
5. All subsequent requests include sessionid cookie
6. Backend validates session on each request
7. Protected routes check isAuthenticated before allowing access
```

### Session Cookie Settings
```
Name: sessionid
Max Age: 2 weeks (1209600 seconds)
HttpOnly: false (development - allows JS access)
SameSite: Lax
Secure: false (development - HTTP)
Path: /
Domain: None (allows localhost and 127.0.0.1)
```

## Authentication State Management (Pinia Store)

### Auth Store State
```typescript
user: User | null           // Current user object
initialized: boolean        // Has checkAuth() been called?
loading: boolean           // Is request in progress?
error: string | null       // Last error message
```

### Auth Store Actions
```typescript
checkAuth()                // Verify session by calling GET /api/auth/me/
signUp(credentials)        // Register new user
signIn(credentials)        // Login user
signOut()                  // Logout user
clearError()              // Clear error message
```

### Router Guard Flow
```typescript
beforeEach():
  1. Check if auth store initialized
     - No: Call checkAuth() to verify session
  2. Check route meta.requiresAuth
     - Yes + Not authenticated: Redirect to /please-signin
  3. Check route meta.requiresGuest
     - Yes + Authenticated: Redirect to /profile
  4. Otherwise: Allow navigation
```

## Error Handling

### Common Errors Fixed
```
❌ [Vue Router warn]: No match found for location with path "/auth/me"
   ✅ Fixed: Removed /auth/me route, use /profile instead

❌ 403 Forbidden on /api/auth/me/ after login
   ✅ Fixed: Explicit session cookie handling in backend

❌ Session not persisting across page refreshes
   ✅ Fixed: CORS_EXPOSE_HEADERS and SESSION_COOKIE_PATH settings

❌ Navigation errors after sign in
   ✅ Fixed: Proper redirect to /profile in SignIn.vue
```

## Summary

The application now has a clear, organized route structure:
- **Public pages**: Marketing and information
- **Auth pages**: User registration and login
- **Profile pages**: User dashboard and book management
- **Book pages**: Individual book operations

All navigation is working correctly with proper authentication guards and session management.
