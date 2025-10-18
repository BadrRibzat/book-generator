#!/bin/bash

# Quick Test Script for Navigation & Authentication Fix
# This script helps verify that the fixes are working correctly

echo "======================================"
echo "Book Generator - Navigation Test"
echo "======================================"
echo ""

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Run this script from /home/badr/book-generator"
    exit 1
fi

echo "✅ Project directory verified"
echo ""

# Test 1: Check frontend router file
echo "Test 1: Checking router configuration..."
if grep -q "name: 'Profile'" frontend/src/router/index.ts && \
   grep -q "/profile/mybooks" frontend/src/router/index.ts && \
   grep -q "/profile/create" frontend/src/router/index.ts; then
    echo "✅ Router has correct profile routes"
else
    echo "❌ Router configuration issue"
fi
echo ""

# Test 2: Check if SignIn redirects to profile
echo "Test 2: Checking SignIn component..."
if grep -q "'/profile'" frontend/src/views/Auth/SignIn.vue; then
    echo "✅ SignIn redirects to /profile"
else
    echo "❌ SignIn redirect issue"
fi
echo ""

# Test 3: Check backend session settings
echo "Test 3: Checking backend session settings..."
if grep -q "CORS_EXPOSE_HEADERS" backend/backend/settings.py && \
   grep -q "SESSION_COOKIE_PATH" backend/backend/settings.py; then
    echo "✅ Backend session settings configured"
else
    echo "❌ Backend session settings issue"
fi
echo ""

# Test 4: Check backend login view
echo "Test 4: Checking login view enhancement..."
if grep -q "request.session.save()" backend/books/views.py && \
   grep -q "response.set_cookie" backend/books/views.py; then
    echo "✅ Login view has explicit session handling"
else
    echo "❌ Login view issue"
fi
echo ""

# Test 5: Check Layout navigation
echo "Test 5: Checking Layout navigation..."
if grep -q "/profile/mybooks" frontend/src/components/Layout.vue; then
    echo "✅ Layout uses /profile/mybooks"
else
    echo "❌ Layout navigation issue"
fi
echo ""

echo "======================================"
echo "Basic Tests Complete"
echo "======================================"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then test:"
echo "  1. Go to http://localhost:5173"
echo "  2. Click 'Sign In' or go to /auth/signin"
echo "  3. Sign in with test5 / your-password"
echo "  4. Should redirect to /profile (not /auth/me)"
echo "  5. Check browser console - no router warnings"
echo "  6. Check Network tab - session cookie should be set"
echo "  7. Refresh page - should stay logged in"
echo ""
