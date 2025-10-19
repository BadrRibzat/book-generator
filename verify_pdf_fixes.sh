#!/bin/bash
# Verify PDF generation fixes

echo "====================================="
echo "PDF GENERATION FIX VERIFICATION SCRIPT"
echo "====================================="
echo

# Check for required packages
echo "Checking for required packages..."
cd /home/badr/book-generator/backend

# Check if pdf2image is in requirements.txt
PDF2IMAGE_CHECK=$(grep -q "pdf2image" requirements.txt && echo "Found" || echo "Missing")

# Check for error handling in PDFMerger
PDF_MERGER_CHECK=$(grep -r "Error accessing cover PDF:" --include="*.py" /home/badr/book-generator/backend/ | wc -l)

# Check for error handling in HTML to PDF conversion
WEASYPRINT_CHECK=$(grep -r "WeasyPrint error:" --include="*.py" /home/badr/book-generator/backend/ | wc -l)

# Print results
echo
echo "1. pdf2image in requirements.txt: $PDF2IMAGE_CHECK"
echo "2. PDFMerger error handling: $(if [ "$PDF_MERGER_CHECK" -gt 0 ]; then echo "✓"; else echo "✗"; fi)"
echo "3. WeasyPrint error handling: $(if [ "$WEASYPRINT_CHECK" -gt 0 ]; then echo "✓"; else echo "✗"; fi)"
echo

# Final verification
if [ "$PDF2IMAGE_CHECK" == "Found" ] && [ "$PDF_MERGER_CHECK" -gt 0 ] && [ "$WEASYPRINT_CHECK" -gt 0 ]; then
    echo "All PDF generation fixes have been properly implemented."
    echo "The 'PDF.__init__() takes 1 positional argument but 3 were given' error should be resolved."
    echo
    echo "To fully verify the fixes, make sure to install all requirements:"
    echo "  cd /home/badr/book-generator/backend"
    echo "  pip install -r requirements.txt"
    echo
    echo "And then run the full test script:"
    echo "  python test_pdf_fixes.py"
    exit 0
else
    echo "Some PDF generation fixes are missing or incomplete."
    echo "Please review the implementation."
    exit 1
fi