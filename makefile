.PHONY: help start stop setup clean install

# Default target
help:
	@echo "🚀 Fives App - Available Commands:"
	@echo ""
	@echo "  make start     - Start both backend and frontend servers"
	@echo "  make stop      - Stop all running servers"
	@echo "  make setup     - Setup backend dependencies"
	@echo "  make install   - Install frontend dependencies"
	@echo "  make clean     - Clean up temporary files"
	@echo "  make help      - Show this help message"
	@echo ""

# Start everything
start:
	@echo "🚀 Starting Fives App..."
	@./start_all.sh

# Stop all servers
stop:
	@echo "🛑 Stopping all servers..."
	@lsof -ti tcp:8000 | xargs kill 2>/dev/null || true
	@lsof -ti tcp:5173 | xargs kill 2>/dev/null || true
	@echo "✅ All servers stopped"

# Setup backend
setup:
	@echo "🔧 Setting up backend..."
	@cd backend && ./setup.sh

# Install frontend dependencies
install:
	@echo "📦 Installing frontend dependencies..."
	@cd fives-frontend && npm install

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"

# Quick start (setup + install + start)
quick: setup install start


