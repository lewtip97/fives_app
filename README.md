# 🏆 Fives App

A comprehensive football team management application for 5-a-side teams, featuring team management, match logging, player statistics, and performance analytics.

## 🚀 Quick Start

### Option 1: One Command (Recommended)
```bash
# Start everything with one command
make start
```

### Option 2: Automated Script
```bash
# Start both backend and frontend
./start_all.sh
```

### Option 3: Manual Setup
```bash
# Backend
cd backend
./setup.sh
source .venv/bin/activate
python start_server.py

# Frontend (in new terminal)
cd fives-frontend
npm install
npm run dev
```

## 🌐 Access Points

Once running, access your app at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🛠️ Available Commands

```bash
make help      # Show all available commands
make start     # Start both servers
make stop      # Stop all servers
make setup     # Setup backend dependencies
make install   # Install frontend dependencies
make clean     # Clean up temporary files
make quick     # Setup + install + start everything
```

## 📁 Project Structure

```
fives_app/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Business logic
│   │   ├── models.py       # Database models
│   │   └── auth.py         # Authentication
│   ├── requirements.txt     # Python dependencies
│   ├── setup.sh           # Backend setup script
│   └── start_server.py    # Server entry point
├── fives-frontend/         # React frontend
│   ├── src/               # Source code
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite configuration
├── start_all.sh           # Unified startup script
├── start_all.bat          # Windows startup script
├── Makefile               # Project commands
└── README.md              # This file
```

## 🔧 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **PostgreSQL** (for production)

## 📦 Features

### 🏟️ Team Management
- Create and manage teams
- Add/remove players
- Team size configuration
- Player profile pictures

### ⚽ Match Logging
- Record match results
- Track player goals
- Opponent management
- Match history

### 📊 Statistics & Analytics
- Player performance metrics
- Team win/loss records
- Goals per game analysis
- Form tracking
- Interactive charts

### 🔐 Authentication
- Supabase integration
- JWT token handling
- User session management
- Secure API endpoints

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   make stop
   # or manually:
   lsof -ti tcp:8000 | xargs kill
   lsof -ti tcp:5173 | xargs kill
   ```

2. **Backend dependencies missing**
   ```bash
   make setup
   ```

3. **Frontend dependencies missing**
   ```bash
   make install
   ```

4. **Virtual environment issues**
   ```bash
   make clean
   make setup
   ```

### Getting Help

- Check the console output for specific error messages
- Verify all prerequisites are installed
- Ensure ports 8000 and 5173 are available
- Check the browser console for frontend errors

## 🧪 Development

### Backend Development
```bash
cd backend
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest  # Run tests
```

### Frontend Development
```bash
cd fives-frontend
npm run build  # Build for production
npm run lint   # Run linter
```

## 📝 Environment Variables

Create a `.env` file in the backend directory:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
DATABASE_URL=your_database_url
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

**Happy coding! ⚽🚀**
