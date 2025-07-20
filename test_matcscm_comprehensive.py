#!/usr/bin/env python3
"""
Comprehensive test script for MatCSCM class.
Tests all major functionality including the new kappa() function.
"""

import numpy as np
import sys
import traceback
from MatCSCM import MatCSCM, Revision

def test_basic_initialization():
    """Test basic initialization of MatCSCM."""
    print("=" * 60)
    print("Testing Basic Initialization")
    print("=" * 60)
    
    try:
        # Test with default parameters
        material = MatCSCM()
        print(f"✓ Default initialization successful")
        print(f"  - f_c: {material.f_c} MPa")
        print(f"  - dmax: {material.dmax} mm")
        print(f"  - mid: {material.mid}")
        print(f"  - rho: {material.rho}")
        
        # Test with custom parameters
        material_custom = MatCSCM(f_c=50, dmax=25, mid=200)
        print(f"✓ Custom initialization successful")
        print(f"  - f_c: {material_custom.f_c} MPa")
        print(f"  - dmax: {material_custom.dmax} mm")
        print(f"  - mid: {material_custom.mid}")
        
        return True
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        traceback.print_exc()
        return False

def test_ceb_integration():
    """Test CEB data integration."""
    print("\n" + "=" * 60)
    print("Testing CEB Integration")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=40, dmax=20)
        ceb_data = material.ceb_data
        
        print(f"✓ CEB data loaded successfully")
        print(f"  - Poisson's ratio (nu): {ceb_data.nu}")
        print(f"  - Elastic modulus (E): {ceb_data.E:.2f} MPa")
        print(f"  - Tensile strength (f_t): {ceb_data.f_t:.2f} MPa")
        print(f"  - Fracture energy (G_ft): {ceb_data.G_ft:.4f} N/mm")
        
        return True
    except Exception as e:
        print(f"✗ CEB integration failed: {e}")
        traceback.print_exc()
        return False

def test_yield_surface_parameters():
    """Test yield surface parameter calculations."""
    print("\n" + "=" * 60)
    print("Testing Yield Surface Parameters")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        ys = material.yield_surface
        
        # Test compression meridian parameters
        print("Compression Meridian Parameters (REV_3):")
        alpha = ys.alpha(Revision.REV_3)
        lamda = ys.lamda(Revision.REV_3)
        beta = ys.beta(Revision.REV_3)
        theta = ys.theta(Revision.REV_3)
        
        print(f"  - alpha: {alpha:.6f}")
        print(f"  - lambda: {lamda:.6f}")
        print(f"  - beta: {beta:.6f}")
        print(f"  - theta: {theta:.6f}")
        
        # Test shear meridian parameters
        print("\nShear Meridian Parameters (REV_3):")
        alpha_1 = ys.alpha_1(Revision.REV_3)
        lamda_1 = ys.lamda_1(Revision.REV_3)
        beta_1 = ys.beta_1(Revision.REV_3)
        
        print(f"  - alpha_1: {alpha_1:.6f}")
        print(f"  - lambda_1: {lamda_1:.6f}")
        print(f"  - beta_1: {beta_1:.6f}")
        
        # Test tensile meridian parameters
        print("\nTensile Meridian Parameters (REV_3):")
        alpha_2 = ys.alpha_2(Revision.REV_3)
        lamda_2 = ys.lamda_2(Revision.REV_3)
        beta_2 = ys.beta_2(Revision.REV_3)
        
        print(f"  - alpha_2: {alpha_2:.6f}")
        print(f"  - lambda_2: {lamda_2:.6f}")
        print(f"  - beta_2: {beta_2:.6f}")
        
        print("✓ All yield surface parameters calculated successfully")
        return True
        
    except Exception as e:
        print(f"✗ Yield surface parameter calculation failed: {e}")
        traceback.print_exc()
        return False

def test_cap_surface_parameters():
    """Test cap surface parameter calculations."""
    print("\n" + "=" * 60)
    print("Testing Cap Surface Parameters")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        cs = material.cap_surface
        
        print("Cap Surface Parameters (REV_3):")
        kappa_0 = cs.kappa_0(Revision.REV_3)
        R = cs.R(Revision.REV_3)
        W = cs.W(Revision.REV_3)
        D1 = cs.D_1(Revision.REV_3)
        D2 = cs.D_2(Revision.REV_3)
        
        print(f"  - kappa_0 (initial cap position): {kappa_0:.6f}")
        print(f"  - R (ellipticity ratio): {R:.6f}")
        print(f"  - W (max plastic volume strain): {W:.6f}")
        print(f"  - D1: {D1:.6e}")
        print(f"  - D2: {D2:.6e}")
        
        print("✓ All cap surface parameters calculated successfully")
        return True
        
    except Exception as e:
        print(f"✗ Cap surface parameter calculation failed: {e}")
        traceback.print_exc()
        return False

def test_meridian_calculations():
    """Test meridian calculations with sample data."""
    print("\n" + "=" * 60)
    print("Testing Meridian Calculations")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        ys = material.yield_surface
        
        # Test stress invariants
        I_values = np.array([-10, -5, 0, 5, 10, 15, 20])
        
        print("Testing with I1 values:", I_values)
        
        # Compression meridian (TXC)
        txc_values = ys.TXC(I_values, Revision.REV_3)
        print(f"\nTXC (Compression Meridian):")
        for i, (I, txc) in enumerate(zip(I_values, txc_values)):
            print(f"  I1={I:6.1f} → TXC={txc:8.4f}")
        
        # Shear meridian (TOR)
        tor_values = ys.TOR(I_values, Revision.REV_3)
        print(f"\nTOR (Shear Meridian):")
        for i, (I, tor) in enumerate(zip(I_values, tor_values)):
            print(f"  I1={I:6.1f} → TOR={tor:8.4f}")
        
        # Tensile meridian (TXE)
        txe_values = ys.TXE(I_values, Revision.REV_3)
        print(f"\nTXE (Tensile Meridian):")
        for i, (I, txe) in enumerate(zip(I_values, txe_values)):
            print(f"  I1={I:6.1f} → TXE={txe:8.4f}")
        
        print("✓ All meridian calculations completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Meridian calculations failed: {e}")
        traceback.print_exc()
        return False

def test_kappa_function():
    """Test the new kappa() function."""
    print("\n" + "=" * 60)
    print("Testing Kappa Function")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        cs = material.cap_surface
        
        # Test parameters
        delta_epsilon_p = 0.001  # Plastic strain increment
        epsilon_v_p_old = 0.0    # Initial plastic volumetric strain
        kappa_0 = 10.0           # Initial kappa value
        
        print(f"Input parameters:")
        print(f"  - delta_epsilon_p: {delta_epsilon_p}")
        print(f"  - epsilon_v_p_old: {epsilon_v_p_old}")
        print(f"  - kappa_0: {kappa_0}")
        
        # Calculate new kappa
        kappa_new, epsilon_v_p_new = cs.kappa(
            delta_epsilon_p=delta_epsilon_p,
            epsilon_v_p_old=epsilon_v_p_old,
            kappa_0=kappa_0,
            rev=Revision.REV_3
        )
        
        print(f"\nResults:")
        print(f"  - kappa_new: {kappa_new:.6f}")
        print(f"  - epsilon_v_p_new: {epsilon_v_p_new:.6f}")
        
        # Test multiple increments
        print(f"\nTesting multiple increments:")
        epsilon_v_p = 0.0
        kappa_current = kappa_0
        
        for i in range(5):
            kappa_current, epsilon_v_p = cs.kappa(
                delta_epsilon_p=0.0005,
                epsilon_v_p_old=epsilon_v_p,
                kappa_0=kappa_0,
                rev=Revision.REV_3
            )
            print(f"  Step {i+1}: kappa={kappa_current:.6f}, epsilon_v_p={epsilon_v_p:.6f}")
        
        # Test that kappa cannot go below kappa_0
        print(f"\nTesting kappa minimum constraint:")
        kappa_test, _ = cs.kappa(
            delta_epsilon_p=-0.01,  # Negative increment
            epsilon_v_p_old=0.0,
            kappa_0=kappa_0,
            rev=Revision.REV_3
        )
        print(f"  With negative increment: kappa={kappa_test:.6f} (should be >= {kappa_0})")
        
        if kappa_test >= kappa_0:
            print("  ✓ Minimum constraint satisfied")
        else:
            print("  ✗ Minimum constraint violated")
            return False
        
        print("✓ Kappa function test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Kappa function test failed: {e}")
        traceback.print_exc()
        return False

def test_yield_function():
    """Test the yield function f()."""
    print("\n" + "=" * 60)
    print("Testing Yield Function")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        ys = material.yield_surface
        
        # Test parameters
        I_1 = np.array([5.0, 10.0, 15.0])
        J_2 = np.array([2.0, 4.0, 6.0])
        kappa = np.array([12.0, 15.0, 18.0])
        kappa_0 = 10.0
        
        print(f"Input parameters:")
        print(f"  - I_1: {I_1}")
        print(f"  - J_2: {J_2}")
        print(f"  - kappa: {kappa}")
        print(f"  - kappa_0: {kappa_0}")
        
        # Calculate yield function
        f_values = ys.f(I_1, J_2, kappa, kappa_0, Revision.REV_3)
        
        print(f"\nYield function results:")
        for i, (i1, j2, k, f_val) in enumerate(zip(I_1, J_2, kappa, f_values)):
            status = "elastic" if f_val < 0 else "yield" if abs(f_val) < 1e-6 else "inadmissible"
            print(f"  Point {i+1}: I1={i1:.1f}, J2={j2:.1f}, κ={k:.1f} → f={f_val:.6f} ({status})")
        
        print("✓ Yield function test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Yield function test failed: {e}")
        traceback.print_exc()
        return False

def test_revision_compatibility():
    """Test compatibility with different revisions."""
    print("\n" + "=" * 60)
    print("Testing Revision Compatibility")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        ys = material.yield_surface
        cs = material.cap_surface
        
        revisions = [Revision.REV_1, Revision.REV_2, Revision.REV_3]
        I_test = np.array([10.0])
        
        print("Testing yield surface parameters across revisions:")
        for rev in revisions:
            print(f"\n{rev.name}:")
            try:
                alpha = ys.alpha(rev)
                kappa_0 = cs.kappa_0(rev)
                R = cs.R(rev)
                W = cs.W(rev)
                
                print(f"  - alpha: {alpha:.6f}")
                print(f"  - kappa_0: {kappa_0:.6f}")
                print(f"  - R: {R:.6f}")
                print(f"  - W: {W:.6f}")
                
                # Test TXC calculation
                txc = ys.TXC(I_test, rev)[0]
                print(f"  - TXC(10): {txc:.6f}")
                
            except Exception as e:
                print(f"  ✗ Error with {rev.name}: {e}")
                return False
        
        print("\n✓ All revisions tested successfully")
        return True
        
    except Exception as e:
        print(f"✗ Revision compatibility test failed: {e}")
        traceback.print_exc()
        return False

def test_integration_workflow():
    """Test integrated workflow: kappa update → yield check."""
    print("\n" + "=" * 60)
    print("Testing Integration Workflow")
    print("=" * 60)
    
    try:
        material = MatCSCM(f_c=35)
        ys = material.yield_surface
        cs = material.cap_surface
        
        # Initial state
        I_1 = 12.0
        J_2 = 3.0
        kappa_0 = 10.0
        epsilon_v_p = 0.0
        
        print(f"Initial state:")
        print(f"  - I_1: {I_1}")
        print(f"  - J_2: {J_2}")
        print(f"  - kappa_0: {kappa_0}")
        print(f"  - epsilon_v_p: {epsilon_v_p}")
        
        # Initial yield check
        f_initial = ys.f(np.array([I_1]), np.array([J_2]), 
                        np.array([kappa_0]), kappa_0, Revision.REV_3)[0]
        print(f"\nInitial yield function: f = {f_initial:.6f}")
        
        # Simulate plastic loading steps
        print(f"\nSimulating plastic loading steps:")
        kappa_current = kappa_0
        
        for step in range(3):
            # Apply plastic strain increment
            delta_epsilon_p = 0.001
            kappa_current, epsilon_v_p = cs.kappa(
                delta_epsilon_p=delta_epsilon_p,
                epsilon_v_p_old=epsilon_v_p,
                kappa_0=kappa_0,
                rev=Revision.REV_3
            )
            
            # Check new yield function
            f_new = ys.f(np.array([I_1]), np.array([J_2]), 
                        np.array([kappa_current]), kappa_0, Revision.REV_3)[0]
            
            print(f"  Step {step+1}:")
            print(f"    - kappa: {kappa_current:.6f}")
            print(f"    - epsilon_v_p: {epsilon_v_p:.6f}")
            print(f"    - f: {f_new:.6f}")
        
        print("✓ Integration workflow test completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Integration workflow test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("MatCSCM Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        test_basic_initialization,
        test_ceb_integration,
        test_yield_surface_parameters,
        test_cap_surface_parameters,
        test_meridian_calculations,
        test_kappa_function,
        test_yield_function,
        test_revision_compatibility,
        test_integration_workflow
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())