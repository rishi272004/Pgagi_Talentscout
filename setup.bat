@echo off
REM TalentScout Setup Script for Windows
REM Automates the setup process for the Hiring Assistant chatbot

setlocal enabledelayedexpansion

echo.
echo ===================================================
echo   TalentScout Setup Script for Windows
echo ===================================================
echo.

REM Check Python installation
echo [1/5] Checking Python Installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Found %PYTHON_VERSION%

REM Create virtual environment
echo.
echo [2/5] Setting Up Virtual Environment...
if exist venv (
    echo Virtual environment already exists
    set /p RECREATE="Recreate it? (y/n): "
    if /i "!RECREATE!"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo [OK] Virtual environment recreated
    )
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo [3/5] Activating Virtual Environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install dependencies
echo.
echo [4/5] Installing Dependencies...
python -m pip install --upgrade pip >nul 2>&1
echo [OK] pip upgraded

pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed

REM Create .env file
echo.
echo [5/5] Configuring Environment...
if not exist .env (
    copy .env.example .env
    echo [OK] .env file created
    echo [WARNING] Please edit .env and configure LLM settings
) else (
    echo [OK] .env file already exists
)

REM Create data directory
if not exist data mkdir data
echo [OK] Data directory created

REM Optional: Run demo
echo.
set /p RUN_DEMO="Run demo script to test installation? (y/n): "
if /i "!RUN_DEMO!"=="y" (
    python demo.py
)

REM Final instructions
echo.
echo ===================================================
echo   Setup Complete!
echo ===================================================
echo.
echo TalentScout Hiring Assistant is ready to use!
echo.
echo Next steps:
echo 1. Configure .env file (if not already configured):
echo    - Option A: Use Ollama (free, local)
echo      Download from https://ollama.ai
echo      Then run: ollama serve
echo      Then run: ollama pull mistral
echo    - Option B: Use OpenAI API (requires API key)
echo      Set OPENAI_API_KEY=your_key_here in .env
echo.
echo 2. Run the Streamlit application:
echo    streamlit run app.py
echo.
echo 3. Open in browser:
echo    http://localhost:8501
echo.
echo Documentation:
echo   - Quick Start: QUICKSTART.md
echo   - Full Documentation: README.md
echo   - Deployment: DEPLOYMENT.md
echo.
echo [OK] Enjoy using TalentScout!
echo.

pause
