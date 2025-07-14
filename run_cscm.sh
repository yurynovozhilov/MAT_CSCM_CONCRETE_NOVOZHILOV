#!/bin/bash
# Script to launch Jupyter Notebook with correct virtual environment
# Usage: ./run_jupyter.sh

# Check that we are in the correct directory
if [ ! -d "venv312" ]; then
    echo "❌ Error: venv312 directory not found!"
    echo "   Make sure you are in the project root directory"
    exit 1
fi

# Activate virtual environment
source venv312/bin/activate

echo "🚀 Starting Jupyter Notebook..."
echo "✅ Virtual environment: venv312"
echo "🐍 Python version: $(python --version)"
echo ""
echo "📓 Opening cscm.ipynb..."
echo "   Press Ctrl+C to stop"
echo ""

# Launch Jupyter with CSCM keyword generator
jupyter notebook cscm.ipynb