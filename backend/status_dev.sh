#!/bin/bash
# Check status of all development services

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}BookAI Backend Services Status${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check Redis
echo -e "${YELLOW}Redis Status:${NC}"
if redis-cli ping > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Running${NC} - redis://127.0.0.1:6379/0"
else
    echo -e "  ${RED}✗ Not Running${NC}"
fi

echo ""

# Check Celery Worker
echo -e "${YELLOW}Celery Worker Status:${NC}"
CELERY_PIDS=$(pgrep -f "celery.*worker")
if [ -n "$CELERY_PIDS" ]; then
    echo -e "  ${GREEN}✓ Running${NC} - PIDs: $CELERY_PIDS"
    echo -e "  Workers: $(pgrep -f 'celery.*worker' | wc -l)"
    echo -e "  Log: celery_worker.log"
else
    echo -e "  ${RED}✗ Not Running${NC}"
fi

echo ""

# Check Django Server
echo -e "${YELLOW}Django Server Status:${NC}"
DJANGO_PID=$(pgrep -f "manage.py runserver")
if [ -n "$DJANGO_PID" ]; then
    echo -e "  ${GREEN}✓ Running${NC} - PID: $DJANGO_PID"
    echo -e "  URL: http://127.0.0.1:8000/"
else
    echo -e "  ${RED}✗ Not Running${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"

# Show recent Celery tasks (if Redis is available)
if redis-cli ping > /dev/null 2>&1; then
    echo ""
    echo -e "${YELLOW}Recent Celery Queue Stats:${NC}"
    QUEUE_LENGTH=$(redis-cli -n 0 LLEN celery 2>/dev/null || echo "0")
    echo -e "  Pending tasks: $QUEUE_LENGTH"
fi

echo ""
echo -e "${YELLOW}Quick Commands:${NC}"
echo -e "  Start all: ${BLUE}./start_dev.sh${NC}"
echo -e "  Stop all:  ${BLUE}./stop_dev.sh${NC}"
echo -e "  View logs: ${BLUE}tail -f celery_worker.log${NC}"
echo ""
