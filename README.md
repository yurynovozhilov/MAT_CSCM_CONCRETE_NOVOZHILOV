# MAT_CSCM_CONCRETE_NOVOZHILOV

Continuous Surface Cap Model (CSCM) for concrete material behavior simulation.

**This code was developed during the research for the scientific article:**
*"Precise Calibration of the Continuous Surface Cap Model for Concrete Simulation"* published in Buildings journal (2022).

## 🌐 Try Online with Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV/HEAD?filepath=cscm.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Citation](https://img.shields.io/badge/Citation-Required-red.svg)](CITATION.md)

Launch the interactive Jupyter notebook directly in your browser without any installation!

### 🔧 Binder Environment
The online environment includes:
- Python 3.12 runtime with all dependencies
- Interactive widgets for parameter adjustment
- All experimental data files
- Automatic notebook launch (`cscm.ipynb`)

**First launch may take 5-10 minutes to build. Subsequent launches are much faster.**

For detailed Binder setup information, see [docs/BINDER_SETUP.md](docs/BINDER_SETUP.md).

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
- `cscm.ipynb` - Main Jupyter notebook

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

For detailed migration history and fixes, see [docs/MIGRATION_HISTORY.md](docs/MIGRATION_HISTORY.md).

## 📄 License & Citation

This project is licensed under the MIT License with Citation Requirement - see the [LICENSE](LICENSE) file for details.

### 📚 How to Cite

If you use this software in your research or commercial applications, please cite both the scientific article and the software:

**Primary Citation (Scientific Article):**
```bibtex
@article{novozhilov2022precise,
  title={Precise Calibration of the Continuous Surface Cap Model for Concrete Simulation},
  author={Novozhilov, Yury Vladislavovich and Dmitriev, Andrey Nikolaevich and Mikhaluk, Dmitry Sergeevich},
  journal={Buildings},
  volume={12},
  number={5},
  pages={636},
  year={2022},
  publisher={MDPI},
  doi={10.3390/buildings12050636}
}
```

**Secondary Citation (Software):**
```bibtex
@software{novozhilov2025cscm,
  author = {Novozhilov, Yury},
  title = {MAT_CSCM_CONCRETE_NOVOZHILOV: Continuous Surface Cap Model for Concrete Material Behavior Simulation},
  url = {https://github.com/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV},
  version = {1.0.0},
  year = {2025}
}
```

**Plain text citations:**
1. Novozhilov, Y.V.; Dmitriev, A.N.; Mikhaluk, D.S. Precise Calibration of the Continuous Surface Cap Model for Concrete Simulation. Buildings 2022, 12, 636. https://doi.org/10.3390/buildings12050636
2. Novozhilov, Y. (2025). MAT_CSCM_CONCRETE_NOVOZHILOV: Continuous Surface Cap Model for Concrete Material Behavior Simulation. GitHub repository. https://github.com/yurynovozhilov/MAT_CSCM_CONCRETE_NOVOZHILOV

### ✅ Usage Rights

- ✅ **Commercial use** - You can use this software for commercial purposes
- ✅ **Modification** - You can modify and adapt the code
- ✅ **Distribution** - You can distribute original or modified versions
- ✅ **Private use** - You can use this software privately
- ⚠️ **Citation required** - You must cite both the scientific article and the software in any publications or applications

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
