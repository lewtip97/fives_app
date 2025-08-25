@echo off
chcp 65001 >nul
echo 🚀 Starting Fives App (Backend + Frontend)...

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "fives-frontend" (
    echo ❌ Frontend directory not found
    pause
    exit /b 1
)

echo.
echo 🔧 Starting Backend Server...

REM Start backend in new window
start "Fives Backend" cmd /k "cd backend && .venv\Scripts\activate && python start_server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo.
echo 🎨 Starting Frontend Server...

REM Start frontend in new window
start "Fives Frontend" cmd /k "cd fives-frontend && npm run dev"

echo.
echo 🎉 Fives App is now starting!
echo    🌐 Frontend will be at: http://localhost:5173
echo    🔧 Backend API will be at: http://localhost:8000
echo    📚 API Docs will be at: http://localhost:8000/docs
echo.
echo 💡 Close the command windows to stop the servers
pause
