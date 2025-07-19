import numpy as np

def I_1(sigma_1, sigma_2, sigma_3):
    """
    Calculate first stress invariant I1 = sigma_1 + sigma_2 + sigma_3.
    
    Parameters:
    -----------
    sigma_1 : float or array_like
        First principal stress
    sigma_2 : float or array_like
        Second principal stress  
    sigma_3 : float or array_like
        Third principal stress
        
    Returns:
    --------
    float or array_like
        First stress invariant I1
    """
    return sigma_1 + sigma_2 + sigma_3

def sigma_m(sigma_1, sigma_2, sigma_3):
    """
    return I_1(sigma_1, sigma_2, sigma_3) / 3.0

def S_1(sigma_1, sigma_2, sigma_3):
    return sigma_1 - sigma_m(sigma_1, sigma_2, sigma_3)

def S_2(sigma_1, sigma_2, sigma_3):
    return sigma_2 - sigma_m(sigma_1, sigma_2, sigma_3)

def S_3(sigma_1, sigma_2, sigma_3):
    """
    return sigma_3 - sigma_m(sigma_1, sigma_2, sigma_3)

def J_2(sigma_1, sigma_2, sigma_3):
    """
    Calculate second stress invariant J2 = 0.5 * ((S_1^2 + S_2^2 + S_3^2)).
    
    Parameters:
    -----------
    sigma_1 : float or array_like
        First principal stress
    sigma_2 : float or array_like
        Second principal stress  
    sigma_3 : float or array_like
        Third principal stress
        
    Returns:
    --------
    float or array_like
        Second stress invariant J2
    """
    return 0.5 * (S_1(sigma_1, sigma_2, sigma_3)**2 + 
                  S_2(sigma_1, sigma_2, sigma_3)**2 + 
                  S_3(sigma_1, sigma_2, sigma_3)**2)