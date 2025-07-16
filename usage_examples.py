#!/usr/bin/env python3
"""
Examples and guide for using the MatCSCM class.

This script provides examples and advanced usage patterns for the
object-oriented MatCSCM class implementation.
"""

from MatCSCM import MatCSCM, keyword_to_text, Revision


def basic_usage_example():
    """
    Example showing basic usage of the MatCSCM class.
    """
    print("Basic Usage Example")
    print("=" * 50)
    
    print("\nUsing MatCSCM class:")
    print("from MatCSCM import MatCSCM, keyword_to_text")
    print("mat_cscm = MatCSCM(f_c=35, dmax=19, rho=2.4E-9)")
    print("keyword_data = mat_cscm.generate_keyword()")
    print("result = keyword_to_text(keyword_data) + mat_cscm.get_ceb_output()")
    
    print("\nActual execution:")
    mat_cscm = MatCSCM(f_c=35, dmax=19, rho=2.4E-9)
    keyword_data = mat_cscm.generate_keyword()
    result = keyword_to_text(keyword_data) + mat_cscm.get_ceb_output()
    
    print(f"Generated result length: {len(result)} characters")
    print("First 200 characters of result:")
    print(result[:200] + "..." if len(result) > 200 else result)


def advanced_usage_example():
    """
    Example showing advanced features available in the MatCSCM implementation.
    """
    print("\n\nAdvanced Features in MatCSCM Implementation")
    print("=" * 50)
    
    # Create material instance
    mat = MatCSCM(f_c=40.0, dmax=20.0, rho=2.4E-9)
    
    print("\n1. Access to nested class methods:")
    print(f"   Yield surface alpha: {mat.yield_surface.alpha(Revision.REV_2):.6f}")
    print(f"   Cap surface X0: {mat.cap_surface.X0(Revision.REV_2):.6f}")
    print(f"   Damage parameter B: {mat.damage.B(Revision.REV_1):.6f}")
    print(f"   Strain rate n_t: {mat.strain_rate.n_t(Revision.REV_1):.6f}")
    
    print("\n2. Direct access to CEB data:")
    ceb_data = mat.ceb_data
    print(f"   Tensile strength: {ceb_data['f_t']:.3f} MPa")
    print(f"   Elastic modulus: {ceb_data['E']:.0f} MPa")
    
    print("\n3. Calculate yield surface values:")
    import numpy as np
    I_values = np.array([0, 10, 20, 30])
    txc_values = mat.yield_surface.TXC(I_values, rev=Revision.REV_2)
    print(f"   I values: {I_values}")
    print(f"   TXC values: {txc_values}")
    
    print("\n4. Calculate dynamic increase factors:")
    dif_t = mat.strain_rate.DIF_CSCM_t(rev=Revision.REV_1, strain_rate_max=100)
    dif_c = mat.strain_rate.DIF_CSCM_c(rev=Revision.REV_1, strain_rate_max=100)
    print(f"   Max tensile DIF: {np.max(dif_t[1, :]):.3f}")
    print(f"   Max compressive DIF: {np.max(dif_c[1, :]):.3f}")


def usage_best_practices():
    """
    Best practices for using MatCSCM class.
    """
    print("\n\nBest Practices for MatCSCM Usage")
    print("=" * 50)
    
    practices = [
        "□ Use descriptive variable names following Python conventions (e.g., mat_cscm)",
        "□ Store keyword_data = mat_cscm.generate_keyword() before text generation",
        "□ Leverage advanced features (nested classes, direct parameter access)",
        "□ Access CEB data directly through mat.ceb_data for material properties",
        "□ Use yield_surface, cap_surface, damage, and strain_rate nested classes",
        "□ Test material parameters thoroughly before production use",
        "□ Document material parameters and their sources",
        "□ Consider parameter validation for critical applications"
    ]
    
    for item in practices:
        print(f"  {item}")


if __name__ == "__main__":
    basic_usage_example()
    advanced_usage_example()
    usage_best_practices()
    
    print("\n\nFor more information, see:")
    print("- docs/MatCSCM_README.md")
    print("- example_usage.py")
    print("- test_matcscm.py")