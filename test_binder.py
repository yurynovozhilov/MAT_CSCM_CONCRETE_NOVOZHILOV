#!/usr/bin/env python3
"""
Test script to verify all modules can be imported in Binder environment
"""

def test_imports():
    """Test all required imports for the CSCM concrete model"""
    
    print("Testing basic Python libraries...")
    try:
        import os
        import numpy as np
        import matplotlib.pyplot as plt
        import ipywidgets as widgets
        from IPython.display import display
        from collections import OrderedDict as OD
        print("✅ Basic libraries imported successfully")
    except ImportError as e:
        print(f"❌ Error importing basic libraries: {e}")
        return False
    
    print("\nTesting project modules...")
    
    modules_to_test = ['d3py', 'CEB', 'plotcurves', 'CapModel']
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} module imported successfully")
        except ImportError as e:
            print(f"❌ Error importing {module_name}: {e}")
            return False
    
    print("\n🎉 All modules imported successfully!")
    print("The environment is ready for the CSCM concrete model notebook.")
    return True

if __name__ == "__main__":
    test_imports()