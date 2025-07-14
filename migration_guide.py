#!/usr/bin/env python3
"""
Migration guide from old CSCM implementation to new MatCSCM class.

This script provides compatibility functions and examples for migrating
from the old functional approach to the new object-oriented MatCSCM class.
"""

from MatCSCM import MatCSCM, keyword_to_text


def CSCM(f_c=35, dmax=19, mid=159, rho=2.4E-9, nplot=1, incre=0, 
         irate='on', erode='off', recov='full', itretrc=0, pred='off', 
         repow=1, nh=0, ch=0, pwrc=5, pwrt=1, pmod=0):
    """
    Compatibility wrapper for the old CSCM function.
    
    This function provides backward compatibility with the old CSCM function
    by creating a MatCSCM instance and returning the keyword dictionary.
    
    DEPRECATED: Use MatCSCM class directly for new code.
    """
    print("WARNING: CSCM() function is deprecated. Use MatCSCM class instead.")
    
    mat = MatCSCM(
        f_c=f_c, dmax=dmax, mid=mid, rho=rho, nplot=nplot, incre=incre,
        irate=irate, erode=erode, recov=recov, itretrc=itretrc, pred=pred,
        repow=repow, nh=nh, ch=ch, pwrc=pwrc, pwrt=pwrt, pmod=pmod
    )
    
    return mat.generate_keyword()


def keyword2text(data, wordLength=10, wordNumber=8):
    """
    Compatibility wrapper for the old keyword2text function.
    
    DEPRECATED: Use keyword_to_text function instead.
    """
    print("WARNING: keyword2text() function is deprecated. Use keyword_to_text() instead.")
    return keyword_to_text(data, wordLength, wordNumber)


def CEBout(f_c, dmax, rho=2.4E-9):
    """
    Compatibility wrapper for the old CEBout function.
    
    DEPRECATED: Use MatCSCM.get_ceb_output() method instead.
    """
    print("WARNING: CEBout() function is deprecated. Use MatCSCM.get_ceb_output() instead.")
    
    mat = MatCSCM(f_c=f_c, dmax=dmax, rho=rho)
    return mat.get_ceb_output()


def migration_example():
    """
    Example showing how to migrate from old to new implementation.
    """
    print("Migration Example")
    print("=" * 50)
    
    # OLD WAY (deprecated)
    print("\n1. OLD WAY (deprecated):")
    print("from d3py import CSCM, keyword2text, CEBout")
    print("MAT_CSCM = CSCM(f_c=35, dmax=19, rho=2.4E-9)")
    print("result = keyword2text(MAT_CSCM) + CEBout(35, 19, 2.4E-9)")
    
    # NEW WAY (recommended)
    print("\n2. NEW WAY (recommended):")
    print("from MatCSCM import MatCSCM, keyword_to_text")
    print("mat_cscm = MatCSCM(f_c=35, dmax=19, rho=2.4E-9)")
    print("keyword_data = mat_cscm.generate_keyword()")
    print("result = keyword_to_text(keyword_data) + mat_cscm.get_ceb_output()")
    
    # Demonstrate both approaches
    print("\n3. ACTUAL EXECUTION:")
    
    # Old way (using compatibility functions)
    print("\nUsing compatibility functions:")
    MAT_CSCM = CSCM(f_c=35, dmax=19, rho=2.4E-9)
    result_old = keyword2text(MAT_CSCM) + CEBout(35, 19, 2.4E-9)
    
    # New way
    print("\nUsing new MatCSCM class:")
    mat_cscm = MatCSCM(f_c=35, dmax=19, rho=2.4E-9)
    keyword_data = mat_cscm.generate_keyword()
    result_new = keyword_to_text(keyword_data) + mat_cscm.get_ceb_output()
    
    # Compare results
    print(f"\nResults are identical: {result_old == result_new}")
    print(f"Old result length: {len(result_old)}")
    print(f"New result length: {len(result_new)}")


def advanced_migration_example():
    """
    Example showing advanced features available in the new implementation.
    """
    print("\n\nAdvanced Features in New Implementation")
    print("=" * 50)
    
    # Create material instance
    mat = MatCSCM(f_c=40.0, dmax=20.0, rho=2.4E-9)
    
    print("\n1. Access to nested class methods:")
    print(f"   Yield surface alpha: {mat.yield_surface.alpha(2):.6f}")
    print(f"   Cap surface X0: {mat.cap_surface.X0(2):.6f}")
    print(f"   Damage parameter B: {mat.damage.B(1):.6f}")
    print(f"   Strain rate n_t: {mat.strain_rate.n_t(1):.6f}")
    
    print("\n2. Direct access to CEB data:")
    ceb_data = mat.ceb_data
    print(f"   Tensile strength: {ceb_data['f_t']:.3f} MPa")
    print(f"   Elastic modulus: {ceb_data['E']:.0f} MPa")
    
    print("\n3. Calculate yield surface values:")
    import numpy as np
    I_values = np.array([0, 10, 20, 30])
    txc_values = mat.yield_surface.TXC(I_values, rev=2)
    print(f"   I values: {I_values}")
    print(f"   TXC values: {txc_values}")
    
    print("\n4. Calculate dynamic increase factors:")
    dif_t = mat.strain_rate.DIF_CSCM_t(rev=1, strain_rate_max=100)
    dif_c = mat.strain_rate.DIF_CSCM_c(rev=1, strain_rate_max=100)
    print(f"   Max tensile DIF: {np.max(dif_t[1, :]):.3f}")
    print(f"   Max compressive DIF: {np.max(dif_c[1, :]):.3f}")


def migration_checklist():
    """
    Checklist for migrating existing code.
    """
    print("\n\nMigration Checklist")
    print("=" * 50)
    
    checklist = [
        "□ Replace 'from d3py import CSCM, keyword2text, CEBout' with 'from MatCSCM import MatCSCM, keyword_to_text'",
        "□ Replace 'CSCM(...)' with 'MatCSCM(...)'",
        "□ Replace 'keyword2text(...)' with 'keyword_to_text(...)'",
        "□ Replace 'CEBout(f_c, dmax, rho)' with 'mat_instance.get_ceb_output()'",
        "□ Update variable names from MAT_CSCM to mat_cscm (following Python conventions)",
        "□ Add 'keyword_data = mat_cscm.generate_keyword()' before text generation",
        "□ Consider using new advanced features (nested classes, direct parameter access)",
        "□ Update any custom functions that depend on the old implementation",
        "□ Test thoroughly to ensure results are identical",
        "□ Update documentation and comments"
    ]
    
    for item in checklist:
        print(f"  {item}")


if __name__ == "__main__":
    migration_example()
    advanced_migration_example()
    migration_checklist()
    
    print("\n\nFor more information, see:")
    print("- docs/MatCSCM_README.md")
    print("- example_usage.py")
    print("- test_matcscm.py")