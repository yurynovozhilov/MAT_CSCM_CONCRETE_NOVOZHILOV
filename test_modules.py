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
        ('CapModel', None),
        ('plotcurves', None),
        ('d3py', None),
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
        from CapModel import alpha, lamda, Q_2, TXC, TXE
        from MatCSCM import MatCSCM
        
        # Test CEB module
        f_c = 40.0
        data = CEB(f_c)
        print(f"✅ CEB: f_c={data['f_c']}, f_t={data['f_t']:.2f}")
        
        # Test DIF functions
        dif_c = DIF_c(f_c)
        dif_t = DIF_t(f_c)
        print(f"✅ DIF: compression shape={dif_c.shape}, tension shape={dif_t.shape}")
        
        # Test CapModel functions
        alpha_val = alpha(f_c, rev=3)
        lambda_val = lamda(f_c, rev=3)
        print(f"✅ CapModel: alpha={alpha_val:.2f}, lambda={lambda_val:.2f}")
        
        # Test functions with arrays
        I = np.array([0, 10, 20])
        q2_vals = Q_2(f_c, I, rev=1)
        txc_vals = TXC(f_c, I, rev=1)
        txe_vals = TXE(f_c, I, rev=1)
        print(f"✅ Array functions: Q_2 shape={q2_vals.shape}")
        
        # Test MatCSCM
        mat_cscm = MatCSCM(f_c=f_c)
        cscm_data = mat_cscm.generate_keyword()
        print(f"✅ MatCSCM: MID={cscm_data['MID']['value']}")
        
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
        from CapModel import Q_2, TXC, TXE
        
        # Fixed functions from notebook
        def Q1MC(f_c, I, rev=1):
            return np.sqrt(3)*Q_2(f_c,I,rev)/(1+Q_2(f_c, I, rev))

        def Q2MC(f_c, I, rev=1):
            return TXE(f_c, I, rev)/TXC(f_c, I, rev)

        def Q1WW(f_c, I, rev=1):
            q=(1-pow(Q_2(f_c, I, rev),2))
            return (np.sqrt(3)*q+(2*Q_2(f_c, I, rev)-1)*np.sqrt((3*q)+5*pow(Q_2(f_c, I, rev),2)-4*Q_2(f_c, I, rev)))/(3*q+pow(1-2*Q_2(f_c, I, rev),2))
        
        f_c = 40
        I = np.array([0, 10, 20])
        
        q1mc_result = Q1MC(f_c, I, rev=1)
        q2mc_result = Q2MC(f_c, I, rev=1)
        q1ww_result = Q1WW(f_c, I, rev=1)
        
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