#!/usr/bin/env python3
"""
Script for testing all modules of the MAT_CSCM_CONCRETE_NOVOZHILOV project
Should be run in the venv312 virtual environment
"""

import sys
import os

def test_environment():
    """Check virtual environment"""
    print("🔍 Checking environment...")
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.executable}")
    
    # Check that we are in the correct venv
    if 'venv312' in sys.executable:
        print("✅ Using correct virtual environment venv312")
    else:
        print("⚠️  WARNING: Not using venv312!")
        print("   Activate environment: source activate.sh")
        return False
    return True

def test_imports():
    """Testing module imports"""
    print("\n📦 Testing imports...")
    
    modules_to_test = [
        ('numpy', 'np'),
        ('matplotlib.pyplot', 'plt'),
        ('CEB', None),

        ('plotcurves', None),
        ('transformation', None)
    ]
    
    failed_imports = []
    
    for module_name, alias in modules_to_test:
        try:
            if alias:
                exec(f"import {module_name} as {alias}")
            else:
                exec(f"import {module_name}")
            print(f"✅ {module_name}")
        except ImportError as e:
            print(f"❌ {module_name}: {e}")
            failed_imports.append(module_name)
    
    return len(failed_imports) == 0

def test_basic_functionality():
    """Testing basic functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        import numpy as np
        from CEB import CEB, DIF_c, DIF_t
        from MatCSCM import MatCSCM, Revision
        
        # Test CEB module
        f_c = 40.0
        data = CEB(f_c)
        print(f"✅ CEB: f_c={data['f_c']}, f_t={data['f_t']:.2f}")
        
        # Test DIF functions
        dif_c = DIF_c(f_c)
        dif_t = DIF_t(f_c)
        print(f"✅ DIF: compression shape={dif_c.shape}, tension shape={dif_t.shape}")
        
        # Test MatCSCM
        mat_cscm = MatCSCM(f_c=f_c)
        
        # Test yield surface functions
        alpha_val = mat_cscm.initialize.alpha(Revision.REV_3)
        lambda_val = mat_cscm.initialize.lamda(Revision.REV_3)
        print(f"✅ MatCSCM yield surface: alpha={alpha_val:.2f}, lambda={lambda_val:.2f}")
        
        # Test functions with arrays
        I = np.array([0, 10, 20])
        q2_vals = mat_cscm.evaluate.Q_2(I, rev=Revision.REV_1)
        txc_vals = mat_cscm.initialize.TXC(I, rev=Revision.REV_1)
        txe_vals = mat_cscm.evaluate.TXE(I, rev=Revision.REV_1)
        print(f"✅ Array functions: Q_2 shape={q2_vals.shape}, TXC shape={txc_vals.shape}")
        
        # Test keyword generation
        cscm_data = mat_cscm.generate_keyword()
        print(f"✅ MatCSCM keyword: MID={cscm_data['MID']['value']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Testing error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_notebook_functions():
    """Testing fixed functions from notebook"""
    print("\n📓 Testing notebook functions...")
    
    try:
        import numpy as np
        from MatCSCM import MatCSCM, Revision
        
        # Create MatCSCM instance
        mat = MatCSCM(f_c=40)
        
        # Import yield surface functions from dedicated module
        from yield_functions import Q1MC, Q2MC, Q1WW
        
        I = np.array([0, 10, 20])
        
        q1mc_result = Q1MC(mat, I, rev=Revision.REV_1)
        q2mc_result = Q2MC(mat, I, rev=Revision.REV_1)
        q1ww_result = Q1WW(mat, I, rev=Revision.REV_1)
        
        print(f"✅ Q1MC: result obtained")
        print(f"✅ Q2MC: shape={q2mc_result.shape}")
        print(f"✅ Q1WW: result obtained")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in notebook functions: {e}")
        return False

def main():
    """Main testing function"""
    print("🚀 Testing MAT_CSCM_CONCRETE_NOVOZHILOV project")
    print("=" * 60)
    
    # Check environment
    if not test_environment():
        sys.exit(1)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test functionality
    functionality_ok = test_basic_functionality()
    
    # Test notebook functions
    notebook_ok = test_notebook_functions()
    
    # Final result
    print("\n" + "=" * 60)
    print("📊 TESTING RESULTS:")
    print(f"   Imports: {'✅ PASSED' if imports_ok else '❌ ERRORS'}")
    print(f"   Basic functionality: {'✅ PASSED' if functionality_ok else '❌ ERRORS'}")
    print(f"   Notebook functions: {'✅ PASSED' if notebook_ok else '❌ ERRORS'}")
    
    if imports_ok and functionality_ok and notebook_ok:
        print("\n🎉 ALL TESTS PASSED! Project is ready to use.")
        return 0
    else:
        print("\n⚠️  THERE ARE ISSUES! Check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())