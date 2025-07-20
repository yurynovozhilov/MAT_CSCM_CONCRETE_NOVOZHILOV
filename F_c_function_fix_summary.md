# F_c Function Fix Summary

## Issue Description
The `F_c` function in the CSCM cap surface implementation was missing the dependency on the second deviatoric stress invariant `J_2`. According to the CSCM theory and the comment in the general yield function, `F_c` should depend on `I_1`, `J_2`, and `kappa`.

## Changes Made

### 1. Function Signature Update
**Before:**
```python
def F_c(self, I, kappa, rev=Revision.REV_3):
```

**After:**
```python
def F_c(self, I_1, J_2, kappa, rev=Revision.REV_3):
```

### 2. Mathematical Implementation Update
**Before:**
```python
result = (I - self.L(kappa, kappa_0))
result *= (np.abs(result) + result)
result /= (2 * pow(self.kappa_0(rev), 2))
result = 1 - result
```

**After:**
```python
# Elliptical cap surface equation:
# F_c = 1 - [(I_1 - L)^2 + R^2 * J_2] / kappa^2
# where L is the cap center and R is the cap aspect ratio

term1 = np.power(I_1 - L_kappa, 2)
term2 = R**2 * J_2

result = 1 - (term1 + term2) / np.power(kappa, 2)
```

### 3. Function Calls Updated
Updated all calls to `F_c` to include the `J_2` parameter:

- In `YieldSurface.f()` method (line 669)
- In `uniaxial_compression_response()` function (line 93)

### 4. Documentation Improvements
- Added comprehensive docstring explaining the cap surface theory
- Clarified parameter meanings and mathematical formulation
- Added proper parameter type annotations

## Theoretical Background
The cap surface in CSCM is an elliptical surface in the `I_1`-`√J_2` stress space that represents the yield criterion for hydrostatic compression. The correct mathematical formulation is:

```
F_c = 1 - [(I_1 - L)² + R² × J_2] / κ²
```

Where:
- `I_1` is the first stress invariant
- `J_2` is the second deviatoric stress invariant
- `L(κ, κ_0)` is the cap center position
- `R` is the cap ellipticity ratio
- `κ` is the hardening parameter

## Testing Results
All tests pass successfully:
- ✅ Basic functionality tests
- ✅ Comprehensive MatCSCM tests
- ✅ Cap surface mathematical properties verification
- ✅ Integration with yield function
- ✅ Uniaxial compression response

## Files Modified
- `MatCSCM.py` - Main implementation file
- `test_matcscm_comprehensive.py` - Fixed CEB integration test

The fix ensures that the cap surface function correctly represents the elliptical yield surface in the principal stress space, which is essential for accurate concrete behavior simulation under multiaxial loading conditions.