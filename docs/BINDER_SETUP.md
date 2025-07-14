# Binder Setup and Usage Guide

## 🚀 Quick Launch

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV/HEAD?filepath=cscm.ipynb)

Launch the interactive Jupyter notebook directly in your browser without any installation!

## 📋 What's Included

The Binder environment includes:
- Python 3.12 runtime
- All necessary dependencies (numpy, matplotlib, jupyter, ipywidgets)
- Main notebook: `cscm.ipynb`
- All Python modules: `CEB.py`, `CapModel.py`, `plotcurves.py`, `d3py.py`
- Experimental data files in `data/` directory

## 🔧 Configuration Files

The following files enable Binder support:

### Core Configuration:
- `requirements.txt` - Python package dependencies
- `runtime.txt` - Python version (3.12)
- `.binder/environment.yml` - Conda environment specification
- `apt.txt` - System packages for matplotlib support

### Dependencies:
- numpy>=2.0.0
- matplotlib>=3.5.0
- jupyter>=1.0.0
- ipywidgets>=8.0.0
- notebook>=7.0.0
- jupyterlab>=4.0.0

### System Packages:
- libfreetype6-dev
- libpng-dev
- pkg-config

## 📊 Usage Instructions

1. Click the Binder badge above
2. Wait for the environment to build (first time may take 5-10 minutes)
3. The `cscm.ipynb` notebook will open automatically
4. Run cells to generate concrete material curves and visualizations

## 🔄 Build Process

- **First Launch**: May take 5-10 minutes to build the environment
- **Subsequent Launches**: Much faster (1-2 minutes)
- **Session Timeout**: Binder sessions timeout after ~10 minutes of inactivity
- **No Persistence**: Changes made in Binder are not saved to the repository

## 🧪 Testing

To test the Binder setup locally, you can run:
```bash
python test_binder.py
```

This verifies that all modules can be imported correctly.

## 🔄 Updating Binder Environment

To update the Binder environment:
1. Modify configuration files as needed
2. Push changes to GitHub
3. Binder will automatically rebuild on next launch

## ⚠️ Important Notes

- Binder sessions are temporary and will timeout after inactivity
- Any changes made in Binder are not saved to the repository
- For persistent work, clone the repository locally
- The repository must be public for Binder to work

## 📞 Troubleshooting

If you encounter issues:
1. Check the Binder build logs
2. Verify all configuration files are present in the repository
3. Test imports with `test_binder.py`
4. Ensure the repository is public on GitHub