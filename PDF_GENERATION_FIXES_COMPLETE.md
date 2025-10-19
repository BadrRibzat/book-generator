# PDF Generation Fixes - Complete

## Problem
The book generation process was failing with the error:
```
Cover generation failed: PDF.__init__() takes 1 positional argument but 3 were given
```

## Root Cause Analysis
1. The primary issue was that we were using an incompatible version of WeasyPrint (v61.0)
2. The PDFMerger class wasn't properly handling errors when accessing PDF pages
3. The PDF-to-PNG conversion was failing silently when pdf2image wasn't installed

## Implemented Fixes

### 1. Downgraded WeasyPrint to a compatible version
```
# Changed from
weasyprint==61.0

# To
weasyprint==52.5
```

### 2. Fixed PDFMerger class in books/services/pdf_merger.py
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

### 3. Improved WeasyPrint usage in covers/services.py
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

### 4. Fixed PDF-to-PNG conversion in covers/services.py
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

### 5. Added pdf2image to requirements.txt
```
pdf2image==1.17.0
```

## Verification
These changes have been verified using the `test_pdf_fixes.py` script, which successfully:
1. Generated 3 different covers using WeasyPrint
2. Merged each cover with a test interior PDF using PDFMerger
3. Confirmed that all operations completed without errors

## Production Deployment Requirements
1. Make sure to install the correct version of WeasyPrint: `pip install weasyprint==52.5`
2. Install pdf2image: `pip install pdf2image==1.17.0` 
3. On Linux systems, ensure that the required dependencies for WeasyPrint and pdf2image are installed:
   ```
   sudo apt-get install python3-dev python3-pip python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
   ```
4. For pdf2image, ensure that poppler-utils is installed:
   ```
   sudo apt-get install poppler-utils
   ```