#!/bin/bash

# ============================================================
# Hospital RAG Assistant - Quick Setup Script for Linux/Mac
# ============================================================

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  Hospital RAG Assistant - Setup Wizard                ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.9+ from https://www.python.org"
    exit 1
fi

echo "[✓] Python detected"
python3 --version
echo ""

# Create virtual environment
echo "[1/5] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
fi
echo "[✓] Virtual environment created"
echo ""

# Activate virtual environment
echo "[2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi
echo "[✓] Virtual environment activated"
echo ""

# Install dependencies
echo "[3/5] Installing dependencies (this may take a few minutes)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "[✓] Dependencies installed"
echo ""

# Create .env file
echo "[4/5] Setting up configuration..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    echo ""
    echo "Please configure your environment:"
    echo "- Get SUPABASE_URL and SUPABASE_KEY from https://supabase.com"
    echo "- Get GROQ_API_KEY from https://console.groq.com (FREE)"
    echo "- Get OPENAI_API_KEY from https://platform.openai.com/api-keys (optional)"
    echo ""
    cp .env.example .env
    echo "[✓] .env file created - please edit with your API keys"
else
    echo "[✓] .env file already exists"
fi
echo ""

# Display next steps
echo "[5/5] Setup complete!"
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║  Next Steps:                                           ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║  1. Edit .env with your API keys                      ║"
echo "║     nano .env                                          ║"
echo "║                                                        ║"
echo "║  2. Run Supabase setup:                               ║"
echo "║     - Go to https://supabase.com and create project   ║"
echo "║     - Copy supabase_setup.sql content                 ║"
echo "║     - Paste in Supabase SQL Editor                    ║"
echo "║                                                        ║"
echo "║  3. Start the backend:                                ║"
echo "║     source venv/bin/activate                          ║"
echo "║     python main.py                                    ║"
echo "║                                                        ║"
echo "║  4. In another terminal, start the UI:               ║"
echo "║     source venv/bin/activate                          ║"
echo "║     streamlit run app_ui.py                           ║"
echo "║                                                        ║"
echo "║  5. Test the API (optional):                          ║"
echo "║     python test_api.py path/to/hospital.pdf           ║"
echo "║                                                        ║"
echo "║  Documentation: See README.md                         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
