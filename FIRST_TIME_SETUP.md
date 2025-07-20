# 🚀 First Time Setup Guide

## After Cloning This Repository

When you clone this repository for the first time, you'll need to set up the Python virtual environment. This is **normal and expected** - virtual environments are never included in Git repositories.

### Quick Setup (Recommended)
```bash
# Run the automated setup script
./setup.sh
```

### Manual Setup (Alternative)
```bash
# 1. Create virtual environment
python3 -m venv venv312

# 2. Activate it
source venv312/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install dependencies
pip install -r requirements.txt

# 5. Test installation
python test_modules.py
```

### After Setup
```bash
# Always activate environment before working
source activate.sh

# Launch the CSCM keyword generator
./run_cscm.sh
```

## ❓ Why This Happens

Virtual environments are **intentionally excluded** from Git repositories because:

1. **Platform Dependency**: Contains OS-specific binary files
2. **Size**: Can be 100-500 MB with thousands of files
3. **Security**: May contain local paths and configurations
4. **Best Practice**: Each developer should create their own clean environment

This is standard practice in Python development - you'll encounter this with most Python projects.

## 🔍 What Gets Created

The setup process creates:
- `venv312/` directory with Python 3.12 virtual environment
- All required packages from `requirements.txt`
- Platform-specific binary files and libraries

## 🛠️ Troubleshooting

### Python Not Found
```bash
# Install Python 3.12 first
# macOS: brew install python@3.12
# Ubuntu: sudo apt install python3.12
```

### Permission Denied
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x run_cscm.sh
chmod +x activate.sh
```

### Import Errors
```bash
# Make sure virtual environment is activated
source activate.sh

# Reinstall dependencies
pip install -r requirements.txt
```