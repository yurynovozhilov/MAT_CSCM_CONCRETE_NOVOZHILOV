#!/usr/bin/env python3
"""
Example usage of the new kappa() function in MatCSCM.
Demonstrates cap hardening behavior during plastic loading.
"""

import numpy as np
import matplotlib.pyplot as plt
from MatCSCM import MatCSCM, Revision

def demonstrate_kappa_evolution():
    """Demonstrate how kappa evolves during plastic loading."""
    print("=" * 60)
    print("Kappa Evolution During Plastic Loading")
    print("=" * 60)
    
    # Create material instance
    material = MatCSCM(f_c=35, dmax=19)
    
    # Initial parameters
    kappa_0 = 10.0  # Initial kappa value
    epsilon_v_p = 0.0  # Initial plastic volumetric strain
    
    # Simulation parameters
    n_steps = 20
    delta_epsilon_p = 0.0005  # Plastic strain increment per step
    
    # Storage arrays
    steps = []
    kappa_values = []
    epsilon_v_p_values = []
    
    print(f"Initial conditions:")
    print(f"  - kappa_0: {kappa_0}")
    print(f"  - delta_epsilon_p per step: {delta_epsilon_p}")
    print(f"  - Number of steps: {n_steps}")
    print()
    
    # Simulate loading steps
    kappa_current = kappa_0
    for step in range(n_steps):
        # Calculate new kappa
        kappa_current, epsilon_v_p = material.cap_surface.kappa(
            delta_epsilon_p=delta_epsilon_p,
            epsilon_v_p_old=epsilon_v_p,
            kappa_0=kappa_0,
            rev=Revision.REV_3
        )
        
        # Store results
        steps.append(step + 1)
        kappa_values.append(kappa_current)
        epsilon_v_p_values.append(epsilon_v_p)
        
        # Print every 5th step
        if (step + 1) % 5 == 0:
            print(f"Step {step+1:2d}: κ = {kappa_current:8.4f}, εᵖᵥ = {epsilon_v_p:.6f}")
    
    return steps, kappa_values, epsilon_v_p_values

def demonstrate_yield_surface_evolution():
    """Demonstrate how yield surface evolves with kappa changes."""
    print("\n" + "=" * 60)
    print("Yield Surface Evolution")
    print("=" * 60)
    
    # Create material instance
    material = MatCSCM(f_c=35, dmax=19)
    
    # Test stress states
    I_1 = 12.0
    J_2 = 3.0
    kappa_0 = 10.0
    
    print(f"Testing stress state: I₁ = {I_1}, J₂ = {J_2}")
    print(f"Initial kappa: κ₀ = {kappa_0}")
    print()
    
    # Different kappa values to test
    kappa_test_values = [10.0, 12.0, 15.0, 18.0, 20.0]
    
    print("Yield function values for different kappa:")
    for kappa in kappa_test_values:
        f_value = material.yield_surface.f(
            np.array([I_1]), np.array([J_2]), 
            np.array([kappa]), kappa_0, Revision.REV_3
        )[0]
        
        status = "elastic" if f_value < 0 else "yield" if abs(f_value) < 1e-6 else "inadmissible"
        print(f"  κ = {kappa:5.1f} → f = {f_value:8.4f} ({status})")

def plot_kappa_evolution():
    """Create plots showing kappa evolution."""
    print("\n" + "=" * 60)
    print("Creating Plots")
    print("=" * 60)
    
    # Get evolution data
    steps, kappa_values, epsilon_v_p_values = demonstrate_kappa_evolution()
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot kappa evolution
    ax1.plot(steps, kappa_values, 'b-o', linewidth=2, markersize=4)
    ax1.set_xlabel('Loading Step')
    ax1.set_ylabel('κ (kappa)')
    ax1.set_title('Cap Hardening: κ Evolution')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(bottom=0)
    
    # Plot plastic volumetric strain
    ax2.plot(steps, epsilon_v_p_values, 'r-s', linewidth=2, markersize=4)
    ax2.set_xlabel('Loading Step')
    ax2.set_ylabel('εᵖᵥ (Plastic Volumetric Strain)')
    ax2.set_title('Plastic Volumetric Strain Evolution')
    ax2.grid(True, alpha=0.3)
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    plt.tight_layout()
    plt.savefig('/Users/GlukRazor/MAT_CSCM_CONCRETE_NOVOZHILOV/kappa_evolution.png', dpi=150, bbox_inches='tight')
    print("✓ Plot saved as 'kappa_evolution.png'")
    
    return fig

def compare_revisions():
    """Compare kappa behavior across different revisions."""
    print("\n" + "=" * 60)
    print("Comparing Revisions")
    print("=" * 60)
    
    # Create material instance
    material = MatCSCM(f_c=35, dmax=19)
    
    # Test parameters
    delta_epsilon_p = 0.001
    epsilon_v_p_old = 0.0
    kappa_0 = 10.0
    
    revisions = [Revision.REV_1, Revision.REV_2, Revision.REV_3]
    
    print(f"Test parameters:")
    print(f"  - delta_epsilon_p: {delta_epsilon_p}")
    print(f"  - epsilon_v_p_old: {epsilon_v_p_old}")
    print(f"  - kappa_0: {kappa_0}")
    print()
    
    print("Results by revision:")
    for rev in revisions:
        kappa_new, epsilon_v_p_new = material.cap_surface.kappa(
            delta_epsilon_p=delta_epsilon_p,
            epsilon_v_p_old=epsilon_v_p_old,
            kappa_0=kappa_0,
            rev=rev
        )
        
        print(f"  {rev.name}: κ = {kappa_new:8.4f}, εᵖᵥ = {epsilon_v_p_new:.6f}")

def main():
    """Run all demonstrations."""
    print("MatCSCM Kappa Function Demonstration")
    print("=" * 60)
    
    # Run demonstrations
    demonstrate_kappa_evolution()
    demonstrate_yield_surface_evolution()
    compare_revisions()
    
    # Create plots
    try:
        plot_kappa_evolution()
    except Exception as e:
        print(f"Note: Plotting failed (likely no display): {e}")
    
    print("\n" + "=" * 60)
    print("Demonstration Complete!")
    print("=" * 60)
    print("\nKey findings:")
    print("• Kappa increases with plastic loading (cap hardening)")
    print("• Plastic volumetric strain accumulates linearly with loading steps")
    print("• Different revisions show different hardening behaviors")
    print("• Yield surface expands as kappa increases")

if __name__ == "__main__":
    main()