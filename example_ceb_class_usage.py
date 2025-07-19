#!/usr/bin/env python3
"""
Example usage of the refactored CEB class.

This example demonstrates how to use the new CEB class where each property
from the original dictionary is now accessible as a method/property.
"""

import numpy as np
import matplotlib.pyplot as plt
from CEB import CEBClass, CEB, DIF_c, DIF_t, sigma_elastic


def main():
    """Demonstrate CEB class usage."""
    print("CEB Class Usage Examples")
    print("=" * 50)
    
    # Example 1: Using the new CEBClass
    print("\n1. Using CEBClass (new object-oriented approach):")
    print("-" * 50)
    
    # Create CEB instance
    ceb = CEBClass(f_c=40, d_max=16.0, rho=2.4E-9)
    
    # Access properties directly
    print(f"Compressive strength f_c: {ceb.f_c} MPa")
    print(f"Tensile strength f_t: {ceb.f_t:.2f} MPa")
    print(f"Elastic modulus E: {ceb.E:.0f} MPa")
    print(f"Shear modulus G: {ceb.G:.0f} MPa")
    print(f"Bulk modulus K: {ceb.K:.0f} MPa")
    print(f"Poisson's ratio nu: {ceb.nu}")
    print(f"Fracture energy G_ft: {ceb.G_ft:.3f} Nmm/mm²")
    print(f"Plasticity number k: {ceb.k:.2f}")
    
    # Example 2: Using backward compatible function
    print("\n2. Using CEB function (backward compatibility):")
    print("-" * 50)
    
    # Get data as dictionary (old way still works)
    ceb_dict = CEB(f_c=40, d_max=16.0, rho=2.4E-9)
    
    print(f"Compressive strength f_c: {ceb_dict['f_c']} MPa")
    print(f"Tensile strength f_t: {ceb_dict['f_t']:.2f} MPa")
    print(f"Elastic modulus E: {ceb_dict['E']:.0f} MPa")
    print(f"Shear modulus G: {ceb_dict['G']:.0f} MPa")
    print(f"Bulk modulus K: {ceb_dict['K']:.0f} MPa")
    print(f"Poisson's ratio nu: {ceb_dict['nu']}")
    
    # Example 3: Accessing stress-strain curves
    print("\n3. Accessing stress-strain curves:")
    print("-" * 50)
    
    compression_curve = ceb.compression_curve
    tension_curve = ceb.tension_curve
    crack_opening_curve = ceb.crack_opening_curve
    
    print(f"Compression curve shape: {compression_curve.shape}")
    print(f"Tension curve shape: {tension_curve.shape}")
    print(f"Crack opening curve shape: {crack_opening_curve.shape}")
    
    # Example 4: Using utility functions
    print("\n4. Using utility functions:")
    print("-" * 50)
    
    # Dynamic Increase Factors
    dif_c_curve = DIF_c(f_c=40)
    dif_t_curve = DIF_t(f_c=40)
    
    print(f"DIF compression curve shape: {dif_c_curve.shape}")
    print(f"DIF tension curve shape: {dif_t_curve.shape}")
    
    # Elastic stress calculation
    strain = 0.001
    stress = sigma_elastic(f_c=40, strain=strain)
    print(f"Elastic stress for strain {strain}: {stress:.2f} MPa")
    
    # Example 5: Comparing different concrete strengths
    print("\n5. Comparing different concrete strengths:")
    print("-" * 50)
    
    strengths = [25, 35, 45, 55]
    print(f"{'f_c (MPa)':<10} {'f_t (MPa)':<10} {'E (GPa)':<10} {'G_ft':<10}")
    print("-" * 40)
    
    for fc in strengths:
        ceb_temp = CEBClass(f_c=fc)
        print(f"{fc:<10} {ceb_temp.f_t:<10.2f} {ceb_temp.E/1000:<10.1f} {ceb_temp.G_ft:<10.3f}")
    
    # Example 6: Plotting stress-strain curves
    print("\n6. Plotting stress-strain curves:")
    print("-" * 50)
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot compression curve
    strain_c = compression_curve[0, :]
    stress_c = compression_curve[1, :]
    ax1.plot(strain_c * 1000, -stress_c, 'b-', linewidth=2, label='CEB-FIP')
    ax1.set_xlabel('Strain (‰)')
    ax1.set_ylabel('Compressive Stress (MPa)')
    ax1.set_title('Compression Stress-Strain Curve')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Plot tension curve
    strain_t = tension_curve[0, :]
    stress_t = tension_curve[1, :]
    ax2.plot(strain_t * 1000, stress_t, 'r-', linewidth=2, label='CEB-FIP')
    ax2.set_xlabel('Strain (‰)')
    ax2.set_ylabel('Tensile Stress (MPa)')
    ax2.set_title('Tension Stress-Strain Curve')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('ceb_stress_strain_curves.png', dpi=150, bbox_inches='tight')
    print("Stress-strain curves saved as 'ceb_stress_strain_curves.png'")
    
    print("\n" + "=" * 50)
    print("CEB class refactoring completed successfully!")
    print("All original functionality is preserved with improved API.")


if __name__ == "__main__":
    main()