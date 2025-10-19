#!/bin/bash

echo "Verifying router configuration and navigation fixes..."
echo "========================================================="

# Check if the router contains both route patterns
ROUTER_CHECK=$(grep -r "path: '/profile/books/:id'" --include="*.ts" /home/badr/book-generator/frontend/src/router/)
if [ -n "$ROUTER_CHECK" ]; then
    echo "✅ Router configuration has /profile/books/:id route"
else
    echo "❌ Router configuration is missing /profile/books/:id route"
fi

# Check SelectCover.vue links
SELECTCOVER_PROFILE_LINKS=$(grep -r "to=\"/profile/books" --include="SelectCover.vue" /home/badr/book-generator/frontend/src/views/Books/)
if [ -n "$SELECTCOVER_PROFILE_LINKS" ]; then
    echo "✅ SelectCover.vue has correct /profile/books links"
else
    echo "❌ SelectCover.vue doesn't use /profile/books links"
fi

# Check Details.vue links
DETAILS_PROFILE_LINKS=$(grep -r "to=\"/profile/books" --include="Details.vue" /home/badr/book-generator/frontend/src/views/Books/)
if [ -n "$DETAILS_PROFILE_LINKS" ]; then
    echo "✅ Details.vue has correct /profile/books links"
else
    echo "❌ Details.vue doesn't use /profile/books links"
fi

# Check List.vue links
LIST_PROFILE_LINKS=$(grep -r "to=\"/profile/books" --include="List.vue" /home/badr/book-generator/frontend/src/views/Books/)
if [ -n "$LIST_PROFILE_LINKS" ]; then
    echo "✅ List.vue has correct /profile/books links"
else
    echo "❌ List.vue doesn't use /profile/books links"
fi

# Check redirection after cover selection
COVER_REDIRECT=$(grep -r "router.push(\`/profile/books/\${bookId.value}\`)" --include="SelectCover.vue" /home/badr/book-generator/frontend/src/views/Books/)
if [ -n "$COVER_REDIRECT" ]; then
    echo "✅ Cover selection redirects to /profile/books/{id}"
else
    echo "❌ Cover selection doesn't redirect to /profile/books/{id}"
fi

# Count remaining /books/ links that should be updated to /profile/books/
REMAINING_BOOKS_LINKS=$(grep -r "'/books/" --include="*.vue" --include="*.ts" /home/badr/book-generator/frontend/src/ | wc -l)
echo "ℹ️ Found $REMAINING_BOOKS_LINKS remaining instances of '/books/' pattern that might need review"

echo "========================================================="
echo "Verification complete!"
echo "If all checks passed, the routing fixes have been successfully implemented."
echo "If any checks failed, please review those components and ensure they use /profile/books paths."