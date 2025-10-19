#!/bin/bash

echo "Verifying cover selection and PDF generation fixes..."
echo "========================================================="

# Check if the PDF merger fixes have been applied
PDF_MERGER_CHECK=$(grep -r "Fix for \"PDF.__init__() takes 1 positional argument but 3 were given\"" --include="*.py" /home/badr/book-generator/backend/)
if [ -n "$PDF_MERGER_CHECK" ]; then
    echo "✅ PDF merger fix has been applied"
else
    echo "❌ PDF merger fix is missing"
fi

# Check router redirects
ROUTER_REDIRECT_CHECK=$(grep -r "Add a redirect for deep book paths" --include="*.ts" /home/badr/book-generator/frontend/src/)
if [ -n "$ROUTER_REDIRECT_CHECK" ]; then
    echo "✅ Router redirects are in place"
else
    echo "❌ Router redirects are missing"
fi

# Check cover selection UX improvements
COVER_UX_CHECK=$(grep -r "Choose Your Book Cover" --include="*.vue" /home/badr/book-generator/frontend/src/views/Books/)
if [ -n "$COVER_UX_CHECK" ]; then
    echo "✅ Cover selection UX improvements are in place"
else
    echo "❌ Cover selection UX improvements are missing"
fi

# Check for error handling with regenerate covers option
REGENERATE_CHECK=$(grep -r "handleRegenerateCovers" --include="*.vue" /home/badr/book-generator/frontend/src/views/Books/)
if [ -n "$REGENERATE_CHECK" ]; then
    echo "✅ Error handling with regenerate covers option is in place"
else
    echo "❌ Error handling with regenerate covers option is missing"
fi

echo "========================================================="
echo "Verification complete!"
echo "To test your changes, restart both the frontend and backend servers."
echo "Then try to create a new book and proceed through the cover selection process."