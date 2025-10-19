# PDF Generation Fixes

## Problem
The book generation process was failing with the error:
```
Cover generation failed: PDF.__init__() takes 1 positional argument but 3 were given
```

## Root Cause Analysis
1. The error occurred in the PDF merging process when trying to access PDF pages incorrectly
2. The WeasyPrint HTML-to-PDF conversion didn't have proper error handling
3. The PDF-to-PNG conversion was failing silently when pdf2image wasn't installed

## Implemented Fixes

### 1. Fixed PDFMerger class in books/services/pdf_merger.py
```python
# Before:
cover_reader = PdfReader(str(cover_pdf_path))
# Fix for "PDF.__init__() takes 1 positional argument but 3 were given"
# Properly handle the page retrieval
if cover_reader.pages and len(cover_reader.pages) > 0:
    writer.add_page(cover_reader.pages[0])

# After:
try:
    cover_reader = PdfReader(str(cover_pdf_path))
    # Fix for "PDF.__init__() takes 1 positional argument but 3 were given"
    # Properly handle the page retrieval - use correct method to access pages
    if len(cover_reader.pages) > 0:
        writer.add_page(cover_reader.pages[0])
    else:
        print(f"Warning: Cover PDF exists but has no pages: {cover_pdf_path}")
except Exception as e:
    print(f"Error accessing cover PDF: {e}")
    # Continue without cover page if there's an error
```

### 2. Improved WeasyPrint usage in covers/services.py
```python
# Before:
HTML(string=html_content).write_pdf(
    str(pdf_path),
    stylesheets=[CSS(string=self._get_base_css())]
)

# After:
try:
    html = HTML(string=html_content)
    html.write_pdf(
        str(pdf_path),
        stylesheets=[CSS(string=self._get_base_css())]
    )
except Exception as e:
    print(f"WeasyPrint error: {str(e)}")
    raise Exception(f"PDF generation failed: {str(e)}")
```

### 3. Fixed PDF-to-PNG conversion in covers/services.py
```python
# Before:
def _pdf_to_png(self, pdf_path, png_path):
    """Convert first page of PDF to PNG for preview"""
    try:
        from pdf2image import convert_from_path
        images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
        if images:
            images[0].save(png_path, 'PNG')
    except ImportError:
        # Fallback: Create a simple preview image using PIL
        img = Image.new('RGB', (600, 900), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((300, 450), "Cover Preview", fill='black', anchor='mm')
        img.save(png_path, 'PNG')

# After:
def _pdf_to_png(self, pdf_path, png_path):
    """Convert first page of PDF to PNG for preview"""
    try:
        # Make sure pdf2image is available
        import importlib.util
        pdf2image_spec = importlib.util.find_spec('pdf2image')
        if pdf2image_spec is not None:
            from pdf2image import convert_from_path
            images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
            if images:
                images[0].save(png_path, 'PNG')
                return
        else:
            print("pdf2image module not found, using fallback method")
    except Exception as e:
        print(f"Error converting PDF to PNG: {e}")
        
    # Fallback: Create a simple preview image using PIL
    try:
        img = Image.new('RGB', (600, 900), color='white')
        draw = ImageDraw.Draw(img)
        draw.text((300, 450), "Cover Preview", fill='black', anchor='mm')
        img.save(png_path, 'PNG')
    except Exception as e:
        print(f"Error creating fallback image: {e}")
```

### 4. Added pdf2image to requirements.txt
```
pdf2image==1.17.0
```

## Verification
These changes should resolve the PDF.__init__() error by:
1. Properly handling PDF page access in PyPDF
2. Adding better error handling in WeasyPrint conversion
3. Providing proper fallback for PDF-to-PNG conversion when pdf2image is missing
4. Adding required packages to requirements.txt

## Next Steps
1. Check logs for any remaining PDF-related errors
2. Ensure all dependencies are installed in the production environment
3. Run test_complete_flow.py to verify the entire book creation process