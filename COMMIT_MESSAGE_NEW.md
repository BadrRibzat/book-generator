feat: fix UI inconsistencies and cover image display issues

## Key Improvements

### 🖼️ Cover Display & Selection
- Fixed cover image loading and display in cover selection page
- Added improved fallback mechanisms for PDF to PNG conversion 
- Enhanced error handling in cover selection process
- Added file existence validation in CoverSerializer

### 🧩 Component Consistency
- Fixed Layout component path imports in Details.vue and SelectCover.vue
- Updated SelectCover.vue to use common Layout component
- Standardized UI across all book-related pages

### 🔌 API & Integration
- Updated Vite config to properly proxy media URLs from backend
- Added enhanced error logging for cover selection process
- Fixed internal redirect paths between components

### 🛣️ Navigation
- Fixed links to use the `/profile/books` prefix consistently
- Fixed redirection after cover selection

## Files Changed

### Backend
- `backend/books/views.py` - Enhanced error handling for cover selection
- `backend/covers/serializers.py` - Added file existence validation
- `backend/covers/services.py` - Improved PDF to PNG conversion with fallbacks

### Frontend
- `frontend/vite.config.ts` - Added proxy for media files
- `frontend/src/views/Books/Details.vue` - Fixed Layout import
- `frontend/src/views/Books/SelectCover.vue` - Fixed Layout import
- `frontend/src/views/Books/Create.vue` - Fixed redirect paths

## Bug Fixes
- ✅ Fixed UI inconsistency between book list and cover selection views
- ✅ Fixed media file serving for cover images
- ✅ Fixed "Failed to select cover" error
- ✅ Fixed layout import path issues
- ✅ Improved loading states and error handling

## Testing
- ✅ Consistent UI across all pages
- ✅ Cover image loading and display
- ✅ Cover selection process

---

**Developer**: Badr Ribzat  
**Date**: October 19, 2025