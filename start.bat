@echo off
chcp 65001 >nul
title Marriage Admin System - Production Mode

echo ========================================
echo    Marriage Admin System - Launcher
echo       Production Mode
echo ========================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python is ready

echo [2/3] Starting services...

:: 启动后端服务
start /b "Backend" cmd /c "cd /d "%SCRIPT_DIR%backend" && python main.py"
timeout /t 3 /nobreak >nul

:: 启动前端静态文件服务器（使用构建后的dist目录）
start /b "Frontend" cmd /c "cd /d "%SCRIPT_DIR%frontend\dist" && python -m http.server 8080"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo    Started successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:8080
echo.
echo [INFO] Opening frontend in browser...
start http://localhost:8080
echo.
echo [INFO] Services are running in background. To stop them, you need to kill the Python processes manually.