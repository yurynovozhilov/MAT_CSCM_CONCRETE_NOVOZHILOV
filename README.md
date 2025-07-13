# MAT_CSCM_CONCRETE_NOVOZHILOV

Continuous Surface Cap Model (CSCM) for concrete material behavior simulation.

## 🚀 Quick Start

### Virtual Environment Activation
```bash
# Activate environment (required!)
source activate.sh
```

### Launch Main Notebook
```bash
# Start Jupyter Notebook
./run_jupyter.sh
```

### Module Testing
```bash
# Test all modules
python test_modules.py
```

## 📋 Requirements

- Python 3.12 (uses virtual environment `venv312`)
- All dependencies installed in `venv312`

## 🔧 VS Code Setup

VS Code is automatically configured to use the correct Python interpreter from `venv312`. Settings are located in `.vscode/settings.json`.

## 📁 Project Structure

### Main modules (Python 3 compatible):
- `CEB.py` - CEB-FIP model for concrete properties
- `CapModel.py` - CSCM yield surface model  
- `plotcurves.py` - Plotting utilities
- `d3py.py` - 3D visualization and CSCM generation functions
- `transformation.py` - Coordinate transformation utilities
- `curves.ipynb` - Main Jupyter notebook

### Helper files:
- `activate.sh` - Environment activation script
- `run_jupyter.sh` - Jupyter launch script
- `test_modules.py` - Module testing script

### Archive files:
- `arc/` - Old code versions (Python 2, not used)

## ⚠️ Important

**Always use the `venv312` virtual environment!**

All commands should be executed after environment activation:
```bash
source activate.sh
```

## 📊 Compatibility Status

✅ **Python 3.12** - Full compatibility  
✅ **All main modules** - Tested and working  
✅ **Jupyter Notebook** - Functions fixed, ready to use  
✅ **VS Code** - Automatic interpreter selection configured
