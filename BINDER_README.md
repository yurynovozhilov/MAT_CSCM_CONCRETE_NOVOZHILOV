# Binder Setup for CSCM Concrete Model

This repository is configured to work with [mybinder.org](https://mybinder.org) for interactive Jupyter notebook execution.

## 🚀 Launch on Binder

Click the badge below to launch the interactive environment:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV/HEAD?filepath=cscm.ipynb)

## 📋 What's Included

The Binder environment includes:
- Python 3.12 runtime
- All necessary dependencies (numpy, matplotlib, jupyter, ipywidgets)
- Main notebook: `cscm.ipynb`
- All Python modules: `CEB.py`, `CapModel.py`, `plotcurves.py`, `d3py.py`
- Experimental data files in `data/` directory

## 🔧 Binder Configuration Files

- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification
- `postBuild` - Post-installation setup script
- `apt.txt` - System packages

## 📊 Usage

1. Click the Binder badge above
2. Wait for the environment to build (first time may take a few minutes)
3. The `cscm.ipynb` notebook will open automatically
4. Run cells to generate concrete material curves and visualizations

## 🔄 Updating

To update the Binder environment:
1. Modify the configuration files as needed
2. Push changes to your GitHub repository
3. Binder will automatically rebuild on next launch

## ⚠️ Notes

- Binder sessions are temporary and will timeout after inactivity
- Any changes made in Binder are not saved to the repository
- For persistent work, clone the repository locally