#!/usr/bin/env python3
"""
Test for checking IRETRC widget functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from MatCSCM import MatCSCM, keyword_to_text

def test_iretrc_functionality():
    """Tests IRETRC parameter functionality"""
    
    print("=== IRETRC Widget Test ===")
    
    # Test with IRETRC = 0 (default)
    print("\n1. Test with IRETRC = 0 (Cap does not retract):")
    mat_0 = MatCSCM(f_c=35, itretrc=0)
    result_0 = mat_0.generate_keyword()
    print(f"   ITRETRC value: {result_0['ITRETRC']['value']}")
    
    # Test with IRETRC = 1 (Cap retracts)
    print("\n2. Test with IRETRC = 1 (Cap retracts):")
    mat_1 = MatCSCM(f_c=35, itretrc=1)
    result_1 = mat_1.generate_keyword()
    print(f"   ITRETRC value: {result_1['ITRETRC']['value']}")
    
    # Check that values are set correctly
    assert result_0['ITRETRC']['value'] == 0, "IRETRC=0 does not work correctly"
    assert result_1['ITRETRC']['value'] == 1, "IRETRC=1 does not work correctly"
    
    print("\n3. Keyword generation with IRETRC=1:")
    keyword_text = keyword_to_text(result_1)
    print(keyword_text[:200] + "...")
    
    # Check that ITRETRC is present in the output
    assert "ITRETRC" in keyword_text, "ITRETRC not found in keyword output"
    
    print("\n✅ All tests passed successfully!")
    print("   IRETRC widget works correctly")
    print("   - Value 0: Cap does not retract (default)")
    print("   - Value 1: Cap retracts")

if __name__ == "__main__":
    test_iretrc_functionality()