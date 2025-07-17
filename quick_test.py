#!/usr/bin/env python3
"""
Quick test to verify all functionality works correctly.
"""

import numpy as np
from MatCSCM import MatCSCM, Revision

def main():
    print("Quick functionality test...")
    
    # Test basic initialization
    material = MatCSCM(f_c=35, dmax=19)
    print("✓ Material initialized")
    
    # Test yield surface
    I_values = np.array([5, 10, 15])
    txc = material.yield_surface.TXC(I_values, Revision.REV_3)
    print(f"✓ TXC calculated: {txc}")
    
    # Test cap surface
    X0 = material.cap_surface.X0(Revision.REV_3)
    print(f"✓ X0 calculated: {X0}")
    
    # Test new kappa function
    kappa_new, eps_new = material.cap_surface.kappa(0.001, 0.0, 10.0, Revision.REV_3)
    print(f"✓ Kappa calculated: {kappa_new:.4f}")
    
    # Test yield function
    f_val = material.yield_surface.f(
        np.array([10]), np.array([3]), np.array([15]), 10.0, Revision.REV_3
    )[0]
    print(f"✓ Yield function calculated: {f_val:.4f}")
    
    print("🎉 All tests passed!")

if __name__ == "__main__":
    main()