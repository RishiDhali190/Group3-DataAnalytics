@echo off
REM Consumer360 - Automated Setup Script for Windows
REM This script sets up the complete full-stack application

echo ========================================
echo   Consumer360 Setup Script
echo   Full-Stack Retail Analytics Platform
echo ========================================
echo.

REM Check if Node.js is installed
echo [1/8] Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)
echo ✓ Node.js is installed
echo.

REM Check if Python is installed
echo [2/8] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo ✓ Python is installed
echo.

REM Check if PostgreSQL is installed
echo [3/8] Checking PostgreSQL installation...
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: PostgreSQL command-line tools not found in PATH
    echo Please ensure PostgreSQL is installed and accessible
    echo You can continue with Docker setup instead
    echo.
) else (
    echo ✓ PostgreSQL is installed
    echo.
)

REM Generate sample data
echo [4/8] Generating sample dataset...
cd data
python generate_sample_data.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to generate sample data
    pause
    exit /b 1
)
cd ..
echo ✓ Sample data generated
echo.

REM Setup Backend
echo [5/8] Setting up Backend (Node.js)...
cd backend
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
)
echo Installing backend dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..
echo ✓ Backend setup complete
echo.

REM Setup Analytics
echo [6/8] Setting up Analytics Engine (Python)...
cd analytics
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
deactivate
cd ..
echo ✓ Analytics engine setup complete
echo.

REM Setup Frontend (if exists)
if exist "frontend" (
    echo [7/8] Setting up Frontend (React)...
    cd frontend
    echo Installing frontend dependencies...
    call npm install
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install frontend dependencies
        pause
        exit /b 1
    )
    cd ..
    echo ✓ Frontend setup complete
    echo.
) else (
    echo [7/8] Frontend directory not found, skipping...
    echo.
)

REM Create database (if PostgreSQL is available)
echo [8/8] Database setup...
echo.
echo IMPORTANT: You need to manually create the PostgreSQL database:
echo.
echo 1. Open PostgreSQL command line or pgAdmin
echo 2. Create database: CREATE DATABASE consumer360_db;
echo 3. Run schema: psql -d consumer360_db -f database\schema.sql
echo 4. Load sample data using the CSV files in the data folder
echo.
echo OR use Docker Compose for automatic setup:
echo    docker-compose up -d
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Configure database connection in backend\.env
echo 2. Start backend:    cd backend ^&^& npm run dev
echo 3. Start analytics:  cd analytics ^&^& venv\Scripts\activate ^&^& python rfm_engine.py
echo 4. Start frontend:   cd frontend ^&^& npm start
echo.
echo OR use Docker:
echo    docker-compose up -d
echo.
echo Access points:
echo   - Frontend:  http://localhost:3000
echo   - Backend:   http://localhost:5000
echo   - pgAdmin:   http://localhost:5050
echo.
echo For detailed instructions, see README_FULLSTACK.md
echo.
pause
