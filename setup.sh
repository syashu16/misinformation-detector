#!/bin/bash

# Quick setup script for Misinformation Detector
# This script sets up the development environment

set -e

echo "🛡️ Setting up Misinformation Detector Development Environment"
echo "================================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_status "Found Python $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip."
    exit 1
fi

print_status "pip3 is available"

# Create virtual environment
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Download NLTK data
print_status "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('vader_lexicon', quiet=True)"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please edit .env file and add your API keys:"
    print_warning "  - GOOGLE_API_KEY (required for AI features)"
    print_warning "  - NEWS_API_KEY (optional)"
else
    print_warning ".env file already exists"
fi

# Create uploads directory
mkdir -p backend/uploads
print_status "Created uploads directory"

# Check if all required environment variables are set
print_status "Checking environment configuration..."
source .env 2>/dev/null || true

if [ -z "$GOOGLE_API_KEY" ] || [ "$GOOGLE_API_KEY" = "your_gemini_api_key_here" ]; then
    print_warning "GOOGLE_API_KEY is not configured. Using demo key: AIzaSyAQqzZ4BNdi-sXEnkyGxZ17qDdKqUEcIPY"
    print_warning "Get your own API key from: https://makersuite.google.com/app/apikey"
fi

if [ -z "$NEWS_API_KEY" ] || [ "$NEWS_API_KEY" = "your_news_api_key_here" ]; then
    print_warning "NEWS_API_KEY is not configured. Using demo key: 712ace18ed8b41228024c65a0847796f"
    print_warning "Get your own API key from: https://newsapi.org/"
fi

# Run a quick test
print_status "Running quick health check..."
cd backend
python -c "
import sys
sys.path.append('.')
try:
    from app import app
    print('✓ Flask app imports successfully')
except ImportError as e:
    print(f'✗ Import error: {e}')
    sys.exit(1)
"

cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run the development server:"
echo "   cd backend && python app.py"
echo "3. Open http://localhost:5000 in your browser"
echo ""
echo "🔧 Useful commands:"
echo "   - Activate venv: source venv/bin/activate"
echo "   - Run tests: pytest tests/"
echo "   - Install new packages: pip install package_name && pip freeze > requirements.txt"
echo "   - Deploy to Cloud Run: ./deploy.sh your-project-id"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Complete project documentation"
echo "   - API_DOCS.md - API reference"
echo "   - PRESENTATION.md - Project presentation"
echo ""
print_status "Happy coding! 🚀"
