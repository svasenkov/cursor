#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a process is running on a port
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null; then
        return 0 # Port is in use
    else
        return 1 # Port is free
    fi
}

# Function to run backend
run_backend() {
    echo -e "${BLUE}Starting backend server...${NC}"
    cd backend
    if ! poetry install; then
        echo -e "${RED}Failed to install backend dependencies${NC}"
        exit 1
    fi
    
    # Check if port 8000 is already in use
    if check_port 8000; then
        echo -e "${RED}Port 8000 is already in use. Please stop the existing process.${NC}"
        exit 1
    fi
    
    poetry run uvicorn app.main:app --reload &
    BACKEND_PID=$!
    echo -e "${GREEN}Backend server started (PID: $BACKEND_PID)${NC}"
    cd ..
    
    # Wait for backend to be ready
    echo "Waiting for backend to be ready..."
    until curl -s http://localhost:8000/health > /dev/null; do
        sleep 1
    done
    echo -e "${GREEN}Backend is ready!${NC}"
}

# Function to run backend tests
run_backend_tests() {
    echo -e "${BLUE}Running backend tests...${NC}"
    cd backend
    if poetry run pytest -v; then
        echo -e "${GREEN}Backend tests passed!${NC}"
        cd ..
        return 0
    else
        echo -e "${RED}Backend tests failed${NC}"
        cd ..
        return 1
    fi
}

# Function to run frontend
run_frontend() {
    echo -e "${BLUE}Starting frontend...${NC}"
    cd frontend
    if ! npm install; then
        echo -e "${RED}Failed to install frontend dependencies${NC}"
        exit 1
    fi
    
    # Check if port 3000 is already in use
    if check_port 3000; then
        echo -e "${RED}Port 3000 is already in use. Please stop the existing process.${NC}"
        exit 1
    fi
    
    npm start &
    FRONTEND_PID=$!
    echo -e "${GREEN}Frontend started (PID: $FRONTEND_PID)${NC}"
    cd ..
}

# Function to cleanup processes on exit
cleanup() {
    echo -e "${BLUE}Cleaning up...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Register cleanup function to run on script exit
trap cleanup EXIT

# Main script
case "$1" in
    "backend")
        run_backend
        # Keep script running
        wait
        ;;
    "test")
        run_backend
        run_backend_tests
        ;;
    "frontend")
        run_frontend
        # Keep script running
        wait
        ;;
    "all")
        run_backend
        run_backend_tests
        run_frontend
        # Keep script running
        wait
        ;;
    *)
        echo "Usage: $0 {backend|test|frontend|all}"
        echo "  backend  - Start backend server"
        echo "  test     - Run backend tests"
        echo "  frontend - Start frontend server"
        echo "  all      - Start both servers and run tests"
        exit 1
        ;;
esac 