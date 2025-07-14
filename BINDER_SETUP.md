# Binder Setup Instructions

## 📋 Files Created for Binder

The following files have been created to enable Binder support:

### Core Configuration Files:
- `requirements.txt` - Python package dependencies
- `runtime.txt` - Python version (3.12)
- `.binder/environment.yml` - Conda environment specification (alternative to requirements.txt)
- `apt.txt` - System packages for matplotlib support
- `postBuild` - Post-installation setup script
- `start` - Custom startup script

### Documentation:
- `BINDER_README.md` - Detailed Binder usage instructions
- `test_binder.py` - Import testing script

## 🚀 How to Use

### Step 1: Upload to GitHub
1. Create a new repository on GitHub (or use existing)
2. Push all files to the repository
3. Make sure the repository is public

### Step 2: Create Binder Link
Your Binder URL is ready:
```
https://mybinder.org/v2/gh/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV/HEAD?filepath=cscm.ipynb
```

### Step 3: Badge Updated
The badge in `README.md` is already configured:
```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV/HEAD?filepath=cscm.ipynb)
```

## 🔧 Configuration Details

### Python Dependencies (requirements.txt):
- numpy>=2.0.0
- matplotlib>=3.5.0
- jupyter>=1.0.0
- ipywidgets>=8.0.0
- notebook>=7.0.0
- jupyterlab>=4.0.0

### System Packages (apt.txt):
- libfreetype6-dev
- libpng-dev
- pkg-config

### Post-Build Setup (postBuild):
- Enables Jupyter widgets
- Installs JupyterLab extensions
- Builds JupyterLab

## 🧪 Testing

To test the setup locally:
```bash
python test_binder.py
```

This will verify that all modules can be imported correctly.

## ⚠️ Important Notes

1. **First Launch**: The first time someone clicks the Binder link, it may take 5-10 minutes to build the environment
2. **Subsequent Launches**: Will be much faster (1-2 minutes)
3. **Session Timeout**: Binder sessions timeout after ~10 minutes of inactivity
4. **No Persistence**: Changes made in Binder are not saved to the repository

## 🔄 Updating

To update the Binder environment:
1. Modify configuration files as needed
2. Push changes to GitHub
3. Binder will automatically rebuild on next launch

## 📞 Support

If you encounter issues:
1. Check the Binder build logs
2. Verify all files are present in the repository
3. Test imports with `test_binder.py`
4. Check that the repository is public