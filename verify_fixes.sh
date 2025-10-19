#!/bin/bash
# Verification script to check if all critical fixes are in place
# Run this script from the root of the book-generator project

# ANSI Color codes for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}Book Generator Fixes Verification Tool${NC}"
echo -e "${BLUE}======================================${NC}"
echo

# Check for Safe ID Conversion in Details.vue
echo -e "${YELLOW}Checking for Safe ID Conversion in Details.vue...${NC}"
if grep -q "const bookId = computed(() => {" frontend/src/views/Books/Details.vue && 
   grep -q "const id = parseInt(props.id);" frontend/src/views/Books/Details.vue &&
   grep -q "return isNaN(id) ? 0 : id;" frontend/src/views/Books/Details.vue; then
  echo -e "${GREEN}✅ Safe ID Conversion found in Details.vue${NC}"
else
  echo -e "${RED}❌ Safe ID Conversion missing in Details.vue${NC}"
fi

# Check for Safe ID Conversion in SelectCover.vue
echo -e "${YELLOW}Checking for Safe ID Conversion in SelectCover.vue...${NC}"
if grep -q "const bookId = computed(() => {" frontend/src/views/Books/SelectCover.vue && 
   grep -q "const id = parseInt(props.id);" frontend/src/views/Books/SelectCover.vue &&
   grep -q "return isNaN(id) ? 0 : id;" frontend/src/views/Books/SelectCover.vue; then
  echo -e "${GREEN}✅ Safe ID Conversion found in SelectCover.vue${NC}"
else
  echo -e "${RED}❌ Safe ID Conversion missing in SelectCover.vue${NC}"
fi

# Check for Auto-polling in Details.vue
echo -e "${YELLOW}Checking for Auto-polling in Details.vue...${NC}"
if grep -q "pollingInterval = ref" frontend/src/views/Books/Details.vue && 
   grep -q "startPolling()" frontend/src/views/Books/Details.vue &&
   grep -q "window.setInterval" frontend/src/views/Books/Details.vue; then
  echo -e "${GREEN}✅ Auto-polling implementation found in Details.vue${NC}"
else
  echo -e "${RED}❌ Auto-polling implementation missing in Details.vue${NC}"
fi

# Check for Enhanced BookSerializer in backend
echo -e "${YELLOW}Checking for Enhanced BookSerializer...${NC}"
if grep -q "user_username = serializers.CharField" backend/books/serializers.py; then
  echo -e "${GREEN}✅ Enhanced BookSerializer with user_username found${NC}"
else
  echo -e "${RED}❌ Enhanced BookSerializer missing user_username field${NC}"
fi

# Check for UI Status display components
echo -e "${YELLOW}Checking for Status-specific UI components...${NC}"
if grep -q "book.status === 'generating'" frontend/src/views/Books/Details.vue && 
   grep -q "book.status === 'content_generated'" frontend/src/views/Books/Details.vue; then
  echo -e "${GREEN}✅ Status-specific UI components found${NC}"
else
  echo -e "${RED}❌ Status-specific UI components missing${NC}"
fi

# Check if all core files exist
echo -e "${YELLOW}Verifying core files exist...${NC}"
MISSING_FILES=0

check_file() {
  if [ -f "$1" ]; then
    echo -e "${GREEN}✅ $1 exists${NC}"
  else
    echo -e "${RED}❌ $1 is missing${NC}"
    MISSING_FILES=$((MISSING_FILES+1))
  fi
}

check_file "frontend/src/views/Books/Details.vue"
check_file "frontend/src/views/Books/SelectCover.vue"
check_file "frontend/src/stores/books.ts"
check_file "backend/books/serializers.py"
check_file "backend/books/views.py"
check_file "backend/books/services/book_generator.py"
check_file "backend/books/services/pdf_merger.py"

if [ $MISSING_FILES -eq 0 ]; then
  echo -e "${GREEN}All core files are present${NC}"
else
  echo -e "${RED}$MISSING_FILES core files are missing${NC}"
fi

echo
echo -e "${BLUE}======================================${NC}"
echo -e "${YELLOW}Verification Summary${NC}"
echo -e "${BLUE}======================================${NC}"
echo
echo -e "The following fixes should be in place:"
echo -e "1. ${YELLOW}Safe ID Conversion${NC} in Details.vue and SelectCover.vue"
echo -e "2. ${YELLOW}Auto-polling${NC} in Details.vue"
echo -e "3. ${YELLOW}Enhanced BookSerializer${NC} in backend/books/serializers.py"
echo -e "4. ${YELLOW}Status-specific UI components${NC} in Details.vue"
echo
echo -e "${BLUE}Next steps:${NC}"
echo -e "1. Run the application and test the book generation flow"
echo -e "2. Check browser console for NaN errors"
echo -e "3. Verify that users stay within the profile workspace during generation"
echo -e "4. Test cover selection and download process"
echo
echo -e "For detailed testing steps, see ${YELLOW}IMPLEMENTATION_VERIFICATION_TESTS.md${NC}"
echo