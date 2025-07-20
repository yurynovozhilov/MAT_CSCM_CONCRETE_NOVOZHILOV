#!/bin/bash
# Setup script for MAT_CSCM_CONCRETE_NOVOZHILOV project
# Run this script after cloning the repository

echo "🚀 Setting up MAT_CSCM_CONCRETE_NOVOZHILOV project..."
echo "============================================================"

# Check if we are in the correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    echo "   Make sure you are in the project root directory"
    exit 1
fi

# Check if venv312 already exists
if [ -d "venv312" ]; then
    echo "⚠️  Virtual environment venv312 already exists"
    read -p "   Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf venv312
    else
        echo "✅ Using existing virtual environment"
        echo "   Run 'source activate.sh' to activate it"
        exit 0
    fi
fi

# Create virtual environment
echo "📦 Creating virtual environment venv312..."
python3 -m venv venv312

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    echo "   Make sure Python 3 is installed"
    exit 1
fi

# Activate virtual environment and upgrade pip
echo "⬆️  Upgrading pip..."
source venv312/bin/activate
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test installation
echo "🧪 Testing installation..."
python -c "from MatCSCM import MatCSCM; from CEB import *; from plotcurves import *; print('✅ All modules imported successfully')"

if [ $? -ne 0 ]; then
    echo "❌ Module import test failed"
    exit 1
fi

echo ""
echo "============================================================"
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Next steps:"
echo "   1. Activate environment: source activate.sh"
echo "   2. Launch notebook: ./run_cscm.sh"
echo "   3. Run tests: python test_modules.py"
echo ""
echo "💡 Tip: Always activate the virtual environment before working"
echo "   with this project using 'source activate.sh'"