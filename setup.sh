#!/bin/bash
# TalentScout Setup Script
# Automates the setup process for the Hiring Assistant chatbot

set -e  # Exit on error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo -e "\n${GREEN}===================================================${NC}"
    echo -e "${GREEN}  $1${NC}"
    echo -e "${GREEN}===================================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check Python installation
print_header "Checking Python Installation"

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org"
    exit 1
fi

python_version=$(python3 --version 2>&1)
print_success "Found: $python_version"

# Create virtual environment
print_header "Setting Up Virtual Environment"

if [ -d "venv" ]; then
    print_warning "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        print_success "Virtual environment recreated"
    fi
else
    python3 -m venv venv
    print_success "Virtual environment created"
fi

# Activate virtual environment
print_header "Activating Virtual Environment"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # macOS/Linux
    source venv/bin/activate
fi

print_success "Virtual environment activated"

# Install dependencies
print_header "Installing Dependencies"

pip install --upgrade pip
print_success "pip upgraded"

pip install -r requirements.txt
print_success "Dependencies installed"

# Create .env file
print_header "Configuring Environment"

if [ ! -f ".env" ]; then
    cp .env.example .env
    print_success ".env file created"
    print_warning "Please edit .env and add your LLM configuration"
else
    print_success ".env file already exists"
fi

# Create data directory
print_header "Creating Data Directory"

mkdir -p data
print_success "Data directory ready"

# Optional: Download Ollama
print_header "LLM Configuration"

echo "Choose your LLM provider:"
echo "1. Ollama (Free, local) - Default"
echo "2. OpenAI API (Requires API key)"
echo "3. Skip for now"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo
        print_warning "Ollama selected"
        echo "To use Ollama:"
        echo "1. Install from: https://ollama.ai"
        echo "2. Run: ollama serve"
        echo "3. Pull model: ollama pull mistral"
        echo
        echo "Your .env is already configured for Ollama"
        ;;
    2)
        echo
        print_warning "OpenAI selected"
        read -p "Enter your OpenAI API key: " api_key
        sed -i "s/LLM_PROVIDER=ollama/LLM_PROVIDER=openai/" .env
        sed -i "s/OPENAI_API_KEY=your_api_key_here/OPENAI_API_KEY=$api_key/" .env
        print_success "OpenAI configuration saved to .env"
        ;;
    3)
        echo
        print_warning "Skipping LLM configuration"
        echo "You can configure later by editing .env"
        ;;
    *)
        echo
        print_error "Invalid choice"
        exit 1
        ;;
esac

# Run demo (optional)
print_header "Running Demo"

read -p "Run demo script to test installation? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 demo.py
fi

# Final instructions
print_header "Setup Complete!"

echo "TalentScout Hiring Assistant is ready to use!"
echo
echo "Next steps:"
echo "1. Activate virtual environment (if not already active):"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    echo "   source venv/Scripts/activate"
else
    echo "   source venv/bin/activate"
fi
echo
echo "2. Start Ollama (if using Ollama):"
echo "   ollama serve"
echo "   (in another terminal: ollama pull mistral)"
echo
echo "3. Run the Streamlit application:"
echo "   streamlit run app.py"
echo
echo "4. Open in browser:"
echo "   http://localhost:8501"
echo
echo "Documentation:"
echo "  - Quick Start: see QUICKSTART.md"
echo "  - Full Docs: see README.md"
echo "  - Deployment: see DEPLOYMENT.md"
echo
print_success "Enjoy using TalentScout!"
