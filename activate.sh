#!/bin/bash
# Script for activating project virtual environment
# Usage: source activate.sh

# Check that we are in the correct directory
if [ ! -d "venv312" ]; then
    echo "Error: venv312 directory not found!"
    echo "Make sure you are in the MAT_CSCM_CONCRETE_NOVOZHILOV project root directory"
    return 1
fi

# Activate virtual environment
source venv312/bin/activate

echo "✅ Virtual environment venv312 activated"
echo "Python version: $(python --version)"
echo "Python path: $(which python)"
echo ""
echo "Available commands:"
echo "  jupyter notebook cscm.ipynb    - launch CSCM keyword generator"
echo "  jupyter notebook curves.ipynb  - launch full notebook with curves"
echo "  python test_modules.py         - test modules"
echo "  deactivate                     - deactivate environment"