@echo off
:: Start Next.js frontend with smart port detection and dependency management
:: Usage: start-frontend.cmd [port]
:: Default port: 3000, fallback: 3001

setlocal EnableDelayedExpansion

:: Set project paths
set FRONTEND_DIR=c:\projects\listacrosseu\frontend
set PROJECT_ROOT=c:\projects\listacrosseu

echo ================================================
echo Next.js Development Server Startup
echo ================================================

:: Check if we're in the correct directory
if not exist "%FRONTEND_DIR%\package.json" (
    echo ERROR: Cannot find package.json in %FRONTEND_DIR%
    echo Make sure the frontend directory exists.
    pause
    exit /b 1
)

:: Change to frontend directory
cd /d %FRONTEND_DIR%
if errorlevel 1 (
    echo ERROR: Failed to navigate to frontend directory
    pause
    exit /b 1
)

:: Check if node_modules exists
if not exist "node_modules" (
    echo Node modules not found. Installing dependencies...
    npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Determine target port
set TARGET_PORT=3000
if not "%1"=="" set TARGET_PORT=%1

echo Checking port %TARGET_PORT% availability...

:: Check if port is in use
netstat -ano | findstr :%TARGET_PORT% >nul
if not errorlevel 1 (
    echo Port %TARGET_PORT% is busy. Checking processes...
    
    :: Show what's using the port
    echo Current processes on port %TARGET_PORT%:
    netstat -ano | findstr :%TARGET_PORT%
    
    echo.
    echo Options:
    echo [1] Kill processes and use port %TARGET_PORT%
    echo [2] Try port 3001 instead
    echo [3] Cancel
    echo.
    set /p choice="Choose option (1-3): "
    
    if "!choice!"=="1" (
        echo Killing processes on port %TARGET_PORT%...
        for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%TARGET_PORT%') do (
            echo Killing PID %%a
            taskkill /PID %%a /F 2>nul
        )
        timeout /t 2 >nul
    ) else if "!choice!"=="2" (
        set TARGET_PORT=3001
        echo Switched to port 3001
    ) else (
        echo Cancelled by user
        pause
        exit /b 0
    )
)

:: Final port check
netstat -ano | findstr :!TARGET_PORT! >nul
if not errorlevel 1 (
    echo ERROR: Port !TARGET_PORT! is still busy after cleanup
    echo Please manually resolve port conflicts
    pause
    exit /b 1
)

:: Clean cache if requested or if previous crash detected
if exist ".next\.next-build-error" (
    echo Previous build error detected. Cleaning cache...
    npm run clean
)

echo.
echo Starting Next.js development server on port !TARGET_PORT!...
echo Press Ctrl+C to stop the server
echo.

:: Start the development server
if !TARGET_PORT!==3000 (
    npm run dev:3000
) else (
    npm run dev:3001
)

echo.
echo Server stopped.
pause