#!/bin/bash
# Development startup script - Starts Django + Celery in one command

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Starting BookAI Backend Development${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Redis is running
echo -e "${YELLOW}Checking Redis...${NC}"
if redis-cli ping > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo -e "${YELLOW}⚠ Redis is not running. Starting Redis...${NC}"
    sudo service redis-server start
    sleep 2
    if redis-cli ping > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Redis started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start Redis. Please start it manually: sudo service redis-server start${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${YELLOW}Starting Celery worker...${NC}"
# Start Celery in background
celery -A backend worker --loglevel=info --logfile=celery_worker.log --detach

# Wait a bit for Celery to start
sleep 2

# Check if Celery started
if pgrep -f "celery.*worker" > /dev/null; then
    echo -e "${GREEN}✓ Celery worker started (PID: $(pgrep -f 'celery.*worker'))${NC}"
else
    echo -e "${YELLOW}⚠ Celery worker may not have started. Check celery_worker.log${NC}"
fi

echo ""
echo -e "${YELLOW}Starting Django development server...${NC}"
echo -e "${GREEN}✓ Django server starting on http://127.0.0.1:8000/${NC}"
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Services Running:${NC}"
echo -e "${GREEN}  • Redis: redis://127.0.0.1:6379/0${NC}"
echo -e "${GREEN}  • Celery Worker: Background process${NC}"
echo -e "${GREEN}  • Django: http://127.0.0.1:8000/${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  • Celery: ${BLUE}tail -f celery_worker.log${NC}"
echo -e "  • Django: ${BLUE}This terminal${NC}"
echo ""
echo -e "${YELLOW}To stop all services: ${BLUE}./stop_dev.sh${NC}"
echo ""

# Start Django server (foreground)
python manage.py runserver
