#!/bin/bash

echo "🔧 Testing Updated API Endpoints..."
echo "=================================="

# Function to test endpoint
test_endpoint() {
    echo "🔍 Testing $1..."
    response=$(curl -s -w "%{http_code}" -X GET "http://127.0.0.1:8000$1" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json" \
        -b cookies.txt)
    
    http_code="${response: -3}"
    body="${response%???}"
    
    if [ "$http_code" -eq 200 ]; then
        echo "✅ $1 - Status: $http_code"
    elif [ "$http_code" -eq 403 ] || [ "$http_code" -eq 401 ]; then
        echo "🔐 $1 - Status: $http_code (Authentication required)"
    else
        echo "❌ $1 - Status: $http_code"
        echo "   Response: $body"
    fi
    echo
}

echo "📋 Testing New Authentication Endpoints:"
test_endpoint "/api/users/profile/"
test_endpoint "/api/users/dashboard/"
test_endpoint "/api/users/subscription-plans/"

echo "📋 Testing Configuration Endpoints:"
test_endpoint "/api/config/sub-niches/"

echo "📋 Testing Books Endpoints:"
test_endpoint "/api/books/"

echo "✅ Endpoint testing complete!"
echo "Note: Authentication-protected endpoints will show 403/401 status"
echo "This is expected behavior when not authenticated."