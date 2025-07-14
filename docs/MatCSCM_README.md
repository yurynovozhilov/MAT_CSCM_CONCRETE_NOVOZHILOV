# MatCSCM Class Documentation

## Overview

The `MatCSCM` class is a comprehensive implementation of the Continuous Surface Cap Model (CSCM) for concrete material behavior simulation. This class replaces the previous functional approach with a well-structured object-oriented design that provides better organization, reusability, and extensibility.

## Key Features

- **Object-oriented design** with nested classes for different functionality groups
- **Complete CSCM implementation** including yield surfaces, damage models, and strain rate effects
- **LS-DYNA keyword generation** for direct use in finite element simulations
- **CEB-FIP integration** for automatic material property estimation
- **Extensible architecture** for easy addition of new features

## Class Structure

### Main Class: `MatCSCM`

The main class handles initialization and coordinates between different model components.

#### Constructor Parameters

```python
MatCSCM(f_c=35, dmax=19, mid=159, rho=2.4E-9, nplot=1, 
        incre=0, irate='on', erode='off', recov='full', 
        itretrc=0, pred='off', repow=1, nh=0, ch=0, 
        pwrc=5, pwrt=1, pmod=0)
```

**Parameters:**
- `f_c` (float): Compressive strength in MPa
- `dmax` (float): Maximum aggregate size in mm
- `mid` (int): Material ID for LS-DYNA
- `rho` (float): Density
- `nplot` (int): Plot option (1-7)
- `incre` (float): Maximum strain increment for subincrementation
- `irate` (str): Rate effects model ('on'/'off')
- `erode` (str): Erosion option ('off' or float value)
- `recov` (str): Modulus recovery option ('full' or float value)
- `itretrc` (int): Cap retraction option (0/1)
- `pred` (str): Preexisting damage ('off' or float value)
- `repow` (float): Power that increases fracture energy with rate effects
- `nh` (float): Hardening initiation
- `ch` (float): Hardening rate
- `pwrc` (float): Shear-to-compression transition parameter
- `pwrt` (float): Shear-to-tension transition parameter
- `pmod` (float): Modify moderate pressure softening parameter

### Nested Classes

#### 1. `YieldSurface`

Handles all yield surface calculations including compression, shear, and tensile meridians.

**Key Methods:**
- `alpha(rev)`, `lamda(rev)`, `beta(rev)`, `theta(rev)`: Compression meridian parameters
- `alpha_1(rev)`, `lamda_1(rev)`, `beta_1(rev)`, `theta_1(rev)`: Shear meridian parameters
- `alpha_2(rev)`, `lamda_2(rev)`, `beta_2(rev)`, `theta_2(rev)`: Tensile meridian parameters
- `F_f(I, rev)`: Shear surface function
- `TXC(I, rev)`: Compression meridian
- `TOR(I, rev)`: Shear meridian
- `TXE(I, rev)`: Tensile meridian
- `Q_1(I, rev)`, `Q_2(I, rev)`: Strength ratios
- `Rubin(I, rev, resolution)`: Rubin yield surface calculation

#### 2. `CapSurface`

Manages cap surface parameters and calculations.

**Key Methods:**
- `X0(rev)`: Initial cap location
- `R(rev)`: Ellipticity ratio
- `W(rev)`: Maximum plastic volume strain
- `D_1(rev)`, `D_2(rev)`: Cap surface parameters
- `L(kappa, kappa_0)`: Cap-shear intersection position
- `X(I, kappa, kappa_0, rev)`: Cap outer edge position
- `F_c(I, kappa, kappa_0, rev)`: Cap failure surface function
- `epsilon_v_p(X, rev)`: Plastic volume strain
- `hydrostatic_compression_parameters(X, rev)`: Hydrostatic compression parameters

#### 3. `Damage`

Handles damage model calculations.

**Key Methods:**
- `B(rev)`: Ductile shape softening parameter
- `D(rev)`: Brittle shape softening parameter
- `pmod()`: Moderate pressure softening parameter
- `brittle_damage(tau_b, D, C, d_max, r_0b)`: Brittle damage calculation
- `ductile_damage(tau_d, B, a, d_max, r_0d)`: Ductile damage calculation

#### 4. `StrainRate`

Manages strain rate effects and dynamic increase factors.

**Key Methods:**
- `n_t(rev)`, `n_c(rev)`: Strain rate exponents
- `eta_0_t(rev)`, `eta_0_c(rev)`: Base fluidity parameters
- `eta_t(strain_rate, rev)`, `eta_c(strain_rate, rev)`: Fluidity parameters
- `overt(rev)`, `overc(rev)`: Over-stress limits
- `DIF_CSCM_t(rev, strain_rate_max)`: Tensile dynamic increase factor
- `DIF_CSCM_c(rev, strain_rate_max)`: Compressive dynamic increase factor

### Main Class Methods

#### `generate_keyword()`

Generates a complete LS-DYNA material keyword dictionary.

**Returns:**
- `dict`: Dictionary containing all material parameters formatted for LS-DYNA

#### `get_ceb_output()`

Generates formatted text output with CEB-FIP material property estimations.

**Returns:**
- `str`: Formatted text with material properties

## Usage Examples

### Basic Usage

```python
from MatCSCM import MatCSCM, keyword_to_text

# Create material instance
mat = MatCSCM(f_c=35.0, dmax=19.0, rho=2.4E-9)

# Generate LS-DYNA keyword
keyword_data = mat.generate_keyword()
keyword_text = keyword_to_text(keyword_data)

# Get CEB output
ceb_output = mat.get_ceb_output()

# Complete output
full_output = keyword_text + ceb_output
print(full_output)
```

### Accessing Nested Class Methods

```python
# Access yield surface parameters
alpha = mat.yield_surface.alpha(rev=2)
lambda_val = mat.yield_surface.lamda(rev=2)

# Calculate yield surface values
import numpy as np
I_values = np.array([0, 10, 20, 30])
txc_values = mat.yield_surface.TXC(I_values, rev=2)

# Access cap surface parameters
X0 = mat.cap_surface.X0(rev=2)
R = mat.cap_surface.R(rev=2)

# Access damage parameters
B = mat.damage.B(rev=1)
D = mat.damage.D(rev=1)

# Calculate dynamic increase factors
dif_t = mat.strain_rate.DIF_CSCM_t(rev=1, strain_rate_max=1000)
dif_c = mat.strain_rate.DIF_CSCM_c(rev=1, strain_rate_max=1000)
```

### Advanced Usage

```python
# Create material with custom parameters
mat = MatCSCM(
    f_c=40.0,           # Higher strength concrete
    dmax=25.0,          # Larger aggregate
    mid=200,            # Custom material ID
    nplot=2,            # Different plot option
    irate='on',         # Enable rate effects
    erode=0.95,         # Custom erosion limit
    recov=0.8           # Partial recovery
)

# Access CEB data directly
ceb_data = mat.ceb_data
print(f"Tensile strength: {ceb_data['f_t']:.3f} MPa")
print(f"Elastic modulus: {ceb_data['E']:.0f} MPa")

# Calculate stress-strain curves
compression_curve = ceb_data['compression_curve']
tension_curve = ceb_data['tension_curve']
```

## Migration from Previous Implementation

### Old Approach (d3py.py)
```python
from d3py import CSCM, keyword2text, CEBout

MAT_CSCM = CSCM(f_c=35, dmax=19, rho=2.4E-9)
result = keyword2text(MAT_CSCM) + CEBout(35, 19, 2.4E-9)
```

### New Approach (MatCSCM.py)
```python
from MatCSCM import MatCSCM, keyword_to_text

mat_cscm = MatCSCM(f_c=35, dmax=19, rho=2.4E-9)
keyword_data = mat_cscm.generate_keyword()
result = keyword_to_text(keyword_data) + mat_cscm.get_ceb_output()
```

## Benefits of the New Implementation

1. **Better Organization**: Related functions are grouped in logical nested classes
2. **Improved Reusability**: Create once, use multiple times with different parameters
3. **Enhanced Extensibility**: Easy to add new methods or modify existing ones
4. **Better Documentation**: Clear class structure with comprehensive docstrings
5. **Type Safety**: Better parameter validation and error handling
6. **Memory Efficiency**: Shared data between methods reduces redundant calculations

## Revision Numbers

The model supports different revision numbers for various parameters:

- **rev=1**: Original implementation
- **rev=2**: Improved formulations (default for most calculations)
- **rev=3**: Latest formulations (default for some parameters)

Choose the appropriate revision based on your specific requirements and validation data.

## Dependencies

- `numpy`: For numerical computations
- `CEB`: For CEB-FIP material property calculations

## Notes

- All stress units are in MPa
- All length units are in mm
- The class automatically handles unit conversions where necessary
- Default parameters are suitable for typical concrete applications
- For specialized applications, consult the CSCM documentation for parameter guidance