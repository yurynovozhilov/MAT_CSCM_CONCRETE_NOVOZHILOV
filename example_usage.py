#!/usr/bin/env python3
"""
Example usage of the MatCSCM class.

This script demonstrates how to use the new MatCSCM class to generate
CSCM material keywords for LS-DYNA.
"""

import numpy as np
from MatCSCM import MatCSCM, keyword_to_text


def main():
    """Main function demonstrating MatCSCM usage."""
    
    # Create CSCM material instance
    print("Creating CSCM material...")
    mat = MatCSCM(
        f_c=35.0,           # Compressive strength (MPa)
        dmax=19.0,          # Maximum aggregate size (mm)
        mid=159,            # Material ID
        rho=2.4E-9,         # Density
        nplot=1,            # Plot option
        irate='on',         # Rate effects
        erode='off',        # Erosion
        recov='full'        # Recovery
    )
    
    # Access nested class methods
    print("\nAccessing yield surface parameters:")
    print(f"Alpha (rev=2): {mat.yield_surface.alpha(2):.6f}")
    print(f"Lambda (rev=2): {mat.yield_surface.lamda(2):.6f}")
    print(f"Beta (rev=2): {mat.yield_surface.beta(2):.6f}")
    print(f"Theta (rev=2): {mat.yield_surface.theta(2):.6f}")
    
    print("\nAccessing cap surface parameters:")
    print(f"X0 (rev=2): {mat.cap_surface.X0(2):.6f}")
    print(f"R (rev=2): {mat.cap_surface.R(2):.6f}")
    print(f"W (rev=2): {mat.cap_surface.W(2):.6f}")
    
    print("\nAccessing damage parameters:")
    print(f"B (rev=1): {mat.damage.B(1):.6f}")
    print(f"D (rev=1): {mat.damage.D(1):.6f}")
    
    print("\nAccessing strain rate parameters:")
    print(f"n_t (rev=1): {mat.strain_rate.n_t(1):.6f}")
    print(f"n_c (rev=1): {mat.strain_rate.n_c(1):.6f}")
    print(f"eta_0_t (rev=1): {mat.strain_rate.eta_0_t(1):.6e}")
    print(f"eta_0_c (rev=1): {mat.strain_rate.eta_0_c(1):.6e}")
    
    # Generate LS-DYNA keyword
    print("\nGenerating LS-DYNA keyword...")
    keyword_data = mat.generate_keyword()
    keyword_text = keyword_to_text(keyword_data)
    
    # Get CEB output
    ceb_output = mat.get_ceb_output()
    
    # Combine results
    full_output = keyword_text + ceb_output
    
    print("\nGenerated LS-DYNA keyword:")
    print("=" * 80)
    print(full_output)
    print("=" * 80)
    
    # Calculate yield surface at different stress states
    print("\nCalculating yield surface values:")
    I_values = np.array([-10, 0, 10, 20, 30])  # First stress invariant values
    
    print("I values:", I_values)
    print("TXC values:", mat.yield_surface.TXC(I_values, rev=2))
    
    # Calculate DIF curves
    print("\nCalculating Dynamic Increase Factors:")
    dif_t = mat.strain_rate.DIF_CSCM_t(rev=1, strain_rate_max=100)
    dif_c = mat.strain_rate.DIF_CSCM_c(rev=1, strain_rate_max=100)
    
    print(f"Tensile DIF curve shape: {dif_t.shape}")
    print(f"Compressive DIF curve shape: {dif_c.shape}")
    print(f"Max tensile DIF: {np.max(dif_t[1, :]):.3f}")
    print(f"Max compressive DIF: {np.max(dif_c[1, :]):.3f}")
    
    # Access CEB data
    print("\nCEB material properties:")
    ceb_data = mat.ceb_data
    print(f"Compressive strength: {ceb_data['f_c']:.1f} MPa")
    print(f"Tensile strength: {ceb_data['f_t']:.3f} MPa")
    print(f"Elastic modulus: {ceb_data['E']:.0f} MPa")
    print(f"Shear modulus: {ceb_data['G']:.0f} MPa")
    print(f"Bulk modulus: {ceb_data['K']:.0f} MPa")
    print(f"Fracture energy (tension): {ceb_data['G_ft']:.6f} N/mm")
    print(f"Fracture energy (compression): {ceb_data['G_fc']:.6f} N/mm")
    
    print("\nExample completed successfully!")


if __name__ == "__main__":
    main()