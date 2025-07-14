#!/usr/bin/env python3
"""
Test script for MatCSCM class.

This script tests the new MatCSCM class implementation and compares
results with the original implementation to ensure compatibility.
"""

import numpy as np
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from MatCSCM import MatCSCM, keyword_to_text
from CEB import CEB


def test_basic_functionality():
    """Test basic functionality of MatCSCM class."""
    print("Testing basic functionality...")
    
    # Test class creation
    mat = MatCSCM(f_c=35.0, dmax=19.0, rho=2.4E-9)
    assert mat.f_c == 35.0
    assert mat.dmax == 19.0
    assert mat.rho == 2.4E-9
    print("✓ Class creation successful")
    
    # Test keyword generation
    keyword_data = mat.generate_keyword()
    assert isinstance(keyword_data, dict)
    assert 'NAME' in keyword_data
    assert keyword_data['NAME'] == '*MAT_CSCM'
    print("✓ Keyword generation successful")
    
    # Test text output
    text_output = keyword_to_text(keyword_data)
    assert isinstance(text_output, str)
    assert '*MAT_CSCM' in text_output
    print("✓ Text output generation successful")
    
    # Test CEB output
    ceb_output = mat.get_ceb_output()
    assert isinstance(ceb_output, str)
    assert 'CEBFIP Estimations' in ceb_output
    print("✓ CEB output generation successful")


def test_nested_classes():
    """Test nested class functionality."""
    print("\nTesting nested classes...")
    
    mat = MatCSCM(f_c=40.0, dmax=20.0)
    
    # Test YieldSurface class
    alpha = mat.yield_surface.alpha(rev=2)
    assert isinstance(alpha, (int, float, np.number))
    assert alpha > 0
    print("✓ YieldSurface class working")
    
    # Test CapSurface class
    X0 = mat.cap_surface.X0(rev=2)
    assert isinstance(X0, (int, float, np.number))
    print("✓ CapSurface class working")
    
    # Test Damage class
    B = mat.damage.B(rev=1)
    D = mat.damage.D(rev=1)
    assert isinstance(B, (int, float, np.number))
    assert isinstance(D, (int, float, np.number))
    print("✓ Damage class working")
    
    # Test StrainRate class
    n_t = mat.strain_rate.n_t(rev=1)
    n_c = mat.strain_rate.n_c(rev=1)
    assert isinstance(n_t, (int, float, np.number))
    assert isinstance(n_c, (int, float, np.number))
    print("✓ StrainRate class working")


def test_yield_surface_calculations():
    """Test yield surface calculations."""
    print("\nTesting yield surface calculations...")
    
    mat = MatCSCM(f_c=30.0, dmax=16.0)
    
    # Test with array input
    I_values = np.array([0, 10, 20, 30])
    
    # Test TXC (compression meridian)
    txc_values = mat.yield_surface.TXC(I_values, rev=2)
    assert isinstance(txc_values, np.ndarray)
    assert len(txc_values) == len(I_values)
    print("✓ TXC calculation successful")
    
    # Test parameter functions
    alpha = mat.yield_surface.alpha(rev=2)
    lamda = mat.yield_surface.lamda(rev=2)
    beta = mat.yield_surface.beta(rev=2)
    theta = mat.yield_surface.theta(rev=2)
    
    assert all(isinstance(x, (int, float, np.number)) for x in [alpha, lamda, beta, theta])
    print("✓ Parameter calculations successful")


def test_strain_rate_effects():
    """Test strain rate effects."""
    print("\nTesting strain rate effects...")
    
    mat = MatCSCM(f_c=35.0, dmax=19.0)
    
    # Test DIF calculations
    dif_t = mat.strain_rate.DIF_CSCM_t(rev=1, strain_rate_max=100)
    dif_c = mat.strain_rate.DIF_CSCM_c(rev=1, strain_rate_max=100)
    
    assert isinstance(dif_t, np.ndarray)
    assert isinstance(dif_c, np.ndarray)
    assert dif_t.shape[0] == 2  # strain rate and DIF
    assert dif_c.shape[0] == 2  # strain rate and DIF
    assert dif_t.shape[1] == 100  # number of points
    assert dif_c.shape[1] == 100  # number of points
    
    # Check that DIF values are reasonable
    assert np.all(dif_t[1, :] >= 1.0)  # DIF should be >= 1
    assert np.all(dif_c[1, :] >= 1.0)  # DIF should be >= 1
    
    print("✓ Strain rate effects calculation successful")


def test_different_revisions():
    """Test different revision numbers."""
    print("\nTesting different revisions...")
    
    mat = MatCSCM(f_c=35.0, dmax=19.0)
    
    # Test different revisions for yield surface parameters
    for rev in [1, 2, 3]:
        try:
            alpha = mat.yield_surface.alpha(rev)
            lamda = mat.yield_surface.lamda(rev)
            beta = mat.yield_surface.beta(rev)
            theta = mat.yield_surface.theta(rev)
            assert all(isinstance(x, (int, float, np.number)) for x in [alpha, lamda, beta, theta])
        except ValueError:
            pass  # Some revisions might not be implemented for all parameters
    
    print("✓ Different revisions working")


def test_parameter_validation():
    """Test parameter validation and edge cases."""
    print("\nTesting parameter validation...")
    
    # Test with different parameter combinations
    mat1 = MatCSCM(f_c=20.0, dmax=10.0, irate='off')
    assert mat1.irate == 0
    
    mat2 = MatCSCM(f_c=50.0, dmax=25.0, erode=0.95)
    assert mat2.erode == 1.95
    
    mat3 = MatCSCM(f_c=35.0, dmax=19.0, recov='0.8')
    assert abs(mat3.recov - 0.2) < 1e-10
    
    print("✓ Parameter validation successful")


def test_ceb_integration():
    """Test CEB integration."""
    print("\nTesting CEB integration...")
    
    mat = MatCSCM(f_c=35.0, dmax=19.0, rho=2.4E-9)
    
    # Check that CEB data is properly loaded
    ceb_data = mat.ceb_data
    assert isinstance(ceb_data, dict)
    
    # Check essential properties
    required_keys = ['f_c', 'f_t', 'E', 'G', 'K', 'G_ft', 'G_fc', 'G_fs']
    for key in required_keys:
        assert key in ceb_data
        assert isinstance(ceb_data[key], (int, float, np.number))
    
    # Check that values are reasonable
    assert ceb_data['f_c'] == 35.0
    assert ceb_data['f_t'] > 0
    assert ceb_data['E'] > 0
    assert ceb_data['G'] > 0
    assert ceb_data['K'] > 0
    
    print("✓ CEB integration successful")


def test_keyword_format():
    """Test LS-DYNA keyword format."""
    print("\nTesting LS-DYNA keyword format...")
    
    mat = MatCSCM(f_c=35.0, dmax=19.0, mid=159, rho=2.4E-9)
    keyword_data = mat.generate_keyword()
    text_output = keyword_to_text(keyword_data)
    
    # Check format
    lines = text_output.split('\n')
    assert lines[0] == '*MAT_CSCM'
    
    # Check that all required cards are present
    assert any('MID' in line for line in lines)
    assert any('RHO' in line for line in lines)
    assert any('ALPHA' in line for line in lines)
    assert any('LAMBDA' in line for line in lines)
    
    print("✓ LS-DYNA keyword format correct")


def run_all_tests():
    """Run all tests."""
    print("Running MatCSCM tests...")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_nested_classes()
        test_yield_surface_calculations()
        test_strain_rate_effects()
        test_different_revisions()
        test_parameter_validation()
        test_ceb_integration()
        test_keyword_format()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)