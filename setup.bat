@echo off
REM Quick setup script for Misinformation Detector (Windows)
REM This script sets up the development environment

echo 🛡️ Setting up Misinformation Detector Development Environment
echo =================================================================

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ Found Python %PYTHON_VERSION%

REM Check if pip is installed
pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ pip is not installed. Please install pip.
    pause
    exit /b 1
)

echo ✓ pip is available

REM Create virtual environment
if not exist "venv" (
    echo ✓ Creating virtual environment...
    python -m venv venv
) else (
    echo ⚠ Virtual environment already exists
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip
echo ✓ Upgrading pip...
pip install --upgrade pip

REM Install requirements
echo ✓ Installing Python dependencies...
pip install -r requirements.txt

REM Download NLTK data
echo ✓ Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('vader_lexicon', quiet=True)"

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ✓ Creating .env file from template...
    copy .env.example .env >nul
    echo ⚠ Please edit .env file and add your API keys:
    echo   - GOOGLE_API_KEY (required for AI features)
    echo   - NEWS_API_KEY (optional)
) else (
    echo ⚠ .env file already exists
)

REM Create uploads directory
if not exist "backend\uploads" mkdir backend\uploads
echo ✓ Created uploads directory

REM Run a quick test
echo ✓ Running quick health check...
cd backend
python -c "import sys; sys.path.append('.'); from app import app; print('✓ Flask app imports successfully')" 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Import error occurred. Please check your installation.
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your API keys
echo 2. Run the development server:
echo    cd backend ^&^& python app.py
echo 3. Open http://localhost:5000 in your browser
echo.
echo 🔧 Useful commands:
echo    - Activate venv: venv\Scripts\activate
echo    - Run tests: pytest tests/
echo    - Install new packages: pip install package_name ^&^& pip freeze ^> requirements.txt
echo    - Deploy to Cloud Run: deploy.bat your-project-id
echo.
echo 📚 Documentation:
echo    - README.md - Complete project documentation
echo    - API_DOCS.md - API reference
echo    - PRESENTATION.md - Project presentation
echo.
echo ✓ Happy coding! 🚀

pause
