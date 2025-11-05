# Fives App Backend

FastAPI backend for the Fives football team management application.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# Make sure you're in the backend directory
cd backend

# Run the setup script
./setup.sh
```

### Option 2: Manual Setup
```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🏃‍♂️ Running the Server

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate

# Start the server
python start_server.py
```

The server will be available at: http://127.0.0.1:8000

## 📦 Dependencies

### Core Dependencies
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM
- **AsyncPG** - Async PostgreSQL driver
- **Databases** - Database query builder
- **Python-Jose** - JWT handling
- **Passlib** - Password hashing
- **Supabase** - Backend-as-a-Service client
- **Pydantic** - Data validation

### Development Dependencies (Optional)
```bash
pip install -r requirements-dev.txt
```

## 🔧 Configuration

Create a `.env` file in the backend directory with:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
DATABASE_URL=your_database_url
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic models
│   ├── auth.py           # Authentication
│   └── database.py       # Database connection
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── setup.sh             # Automated setup script
└── start_server.py      # Server entry point
```

## 🧪 Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests
pytest
```

## 🚨 Troubleshooting

### Common Issues

1. **psycopg2-binary fails to install**
   - This package is optional and commented out in requirements.txt
   - The app uses asyncpg instead

2. **Module not found errors**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Port already in use**
   - Kill processes on port 8000: `lsof -ti tcp:8000 | xargs kill`

### Getting Help

Check the console output for specific error messages. Most issues are related to missing dependencies or incorrect virtual environment setup.
