#!/bin/bash

# Fives App - Start Everything Script
echo "🚀 Starting Fives App (Backend + Frontend)..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${RED}❌ Port $1 is already in use${NC}"
        echo "   Kill existing process: lsof -ti tcp:$1 | xargs kill"
        return 1
    else
        echo -e "${GREEN}✅ Port $1 is available${NC}"
        return 0
    fi
}

# Function to start backend
start_backend() {
    echo -e "\n${BLUE}🔧 Starting Backend Server...${NC}"
    
    # Check if backend directory exists
    if [ ! -d "backend" ]; then
        echo -e "${RED}❌ Backend directory not found${NC}"
        return 1
    fi
    
    cd backend
    
    # Check if virtual environment exists
    if [ ! -d ".venv" ]; then
        echo -e "${YELLOW}⚠️  Virtual environment not found. Running setup...${NC}"
        ./setup.sh
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Backend setup failed${NC}"
            return 1
        fi
    fi
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Check if dependencies are installed
    if ! python -c "import fastapi" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Dependencies not installed. Installing...${NC}"
        pip install -r requirements.txt
    fi
    
    # Start backend server in background
    echo -e "${GREEN}🚀 Starting FastAPI server on port 8000...${NC}"
    python start_server.py &
    BACKEND_PID=$!
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if backend is running
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend server started successfully (PID: $BACKEND_PID)${NC}"
        echo -e "${BLUE}   🌐 Backend API: http://localhost:8000${NC}"
        echo -e "${BLUE}   📚 API Docs: http://localhost:8000/docs${NC}"
    else
        echo -e "${RED}❌ Backend server failed to start${NC}"
        return 1
    fi
    
    cd ..
}

# Function to start frontend
start_frontend() {
    echo -e "\n${BLUE}🎨 Starting Frontend Server...${NC}"
    
    # Check if frontend directory exists
    if [ ! -d "fives-frontend" ]; then
        echo -e "${RED}❌ Frontend directory not found${NC}"
        return 1
    fi
    
    cd fives-frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}⚠️  Node modules not found. Installing...${NC}"
        npm install
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Frontend dependencies failed to install${NC}"
            return 1
        fi
    fi
    
    # Start frontend server in background
    echo -e "${GREEN}🚀 Starting Vite dev server on port 5173...${NC}"
    npm run dev &
    FRONTEND_PID=$!
    
    # Wait a moment for server to start
    sleep 5
    
    # Check if frontend is running
    if curl -s http://localhost:5173/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend server started successfully (PID: $FRONTEND_PID)${NC}"
        echo -e "${BLUE}   🌐 Frontend: http://localhost:5173${NC}"
    else
        echo -e "${RED}❌ Frontend server failed to start${NC}"
        return 1
    fi
    
    cd ..
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    
    if [ ! -z "$BACKEND_PID" ]; then
        echo "   Killing backend server (PID: $BACKEND_PID)"
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        echo "   Killing frontend server (PID: $FRONTEND_PID)"
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    # Kill any remaining processes on our ports
    lsof -ti tcp:8000 | xargs kill 2>/dev/null
    lsof -ti tcp:5173 | xargs kill 2>/dev/null
    
    echo -e "${GREEN}✅ All servers stopped${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Main execution
echo -e "${BLUE}🔍 Checking ports...${NC}"
check_port 8000 || exit 1
check_port 5173 || exit 1

# Start backend
start_backend
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start backend${NC}"
    exit 1
fi

# Start frontend
start_frontend
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start frontend${NC}"
    cleanup
    exit 1
fi

# Success message
echo -e "\n${GREEN}🎉 Fives App is now running!${NC}"
echo -e "${BLUE}   🌐 Frontend: http://localhost:5173${NC}"
echo -e "${BLUE}   🔧 Backend API: http://localhost:8000${NC}"
echo -e "${BLUE}   📚 API Documentation: http://localhost:8000/docs${NC}"
echo -e "\n${YELLOW}💡 Press Ctrl+C to stop all servers${NC}"

# Keep script running and show logs
echo -e "\n${BLUE}📋 Server logs (Ctrl+C to stop):${NC}"
wait
