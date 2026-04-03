@echo off
REM ============================================================
REM Hospital RAG Assistant - Quick Setup Script for Windows
REM ============================================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  Hospital RAG Assistant - Setup Wizard                ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo [✓] Python detected
python --version
echo.

REM Create virtual environment
echo [1/5] Creating Python virtual environment...
if not exist "venv" (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo [✓] Virtual environment created
echo.

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [✓] Virtual environment activated
echo.

REM Install dependencies
echo [3/5] Installing dependencies (this may take a few minutes)...
pip install --upgrade pip -q
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [✓] Dependencies installed
echo.

REM Create .env file
echo [4/5] Setting up configuration...
if not exist ".env" (
    echo Creating .env file from template...
    echo.
    echo Please configure your environment:
    echo - Get SUPABASE_URL and SUPABASE_KEY from https://supabase.com
    echo - Get GROQ_API_KEY from https://console.groq.com (FREE)
    echo - Get OPENAI_API_KEY from https://platform.openai.com/api-keys (optional)
    echo.
    copy .env.example .env
    echo [✓] .env file created - please edit with your API keys
) else (
    echo [✓] .env file already exists
)
echo.

REM Display next steps
echo [5/5] Setup complete!
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  Next Steps:                                           ║
echo ╠════════════════════════════════════════════════════════╣
echo ║  1. Edit .env with your API keys                      ║
echo ║                                                        ║
echo ║  2. Run Supabase setup:                               ║
echo ║     - Go to https://supabase.com and create project   ║
echo ║     - Copy supabase_setup.sql content                 ║
echo ║     - Paste in Supabase SQL Editor                    ║
echo ║                                                        ║
echo ║  3. Start the backend:                                ║
echo ║     python main.py                                    ║
echo ║                                                        ║
echo ║  4. In another terminal, start the UI:               ║
echo ║     streamlit run app_ui.py                           ║
echo ║                                                        ║
echo ║  5. Test the API (optional):                          ║
echo ║     python test_api.py path/to/hospital.pdf           ║
echo ║                                                        ║
echo ║  Documentation: See README.md                         ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Press any key to exit...
pause >nul
