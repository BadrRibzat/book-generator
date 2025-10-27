#!/bin/bash
# Stop all development services

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Stopping BookAI Backend Services${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Stop Celery workers
echo -e "${YELLOW}Stopping Celery workers...${NC}"
pkill -f "celery.*worker"
sleep 1

if pgrep -f "celery.*worker" > /dev/null; then
    echo -e "${YELLOW}⚠ Force killing Celery workers...${NC}"
    pkill -9 -f "celery.*worker"
    sleep 1
fi

if ! pgrep -f "celery.*worker" > /dev/null; then
    echo -e "${GREEN}✓ Celery workers stopped${NC}"
else
    echo -e "${RED}✗ Failed to stop Celery workers${NC}"
fi

echo ""

# Stop Django server
echo -e "${YELLOW}Stopping Django server...${NC}"
pkill -f "manage.py runserver"
sleep 1

if pgrep -f "manage.py runserver" > /dev/null; then
    echo -e "${YELLOW}⚠ Force killing Django server...${NC}"
    pkill -9 -f "manage.py runserver"
    sleep 1
fi

if ! pgrep -f "manage.py runserver" > /dev/null; then
    echo -e "${GREEN}✓ Django server stopped${NC}"
else
    echo -e "${RED}✗ Failed to stop Django server${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}All services stopped${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Note: Redis is still running (system service)${NC}"
echo -e "To stop Redis: ${BLUE}sudo service redis-server stop${NC}"
echo ""
