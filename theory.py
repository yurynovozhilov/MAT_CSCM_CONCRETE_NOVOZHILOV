import numpy as np


class Theory:
    """
    Theory class containing static methods for concrete mechanics calculations.
    
    This class provides methods for calculating elastic moduli, stress invariants,
    and stress deviator components used in concrete material modeling.
    """
    
    @staticmethod
    def G(f_c):
        """
        Calculate shear modulus G from characteristic compressive strength.
        Parameters:
        -----------
        f_c : float
            Characteristic compressive strength of concrete (MPa)
        Returns:
        --------
        float
            Shear modulus G (MPa)
        """ 
        from CEB import CEBClass
        ceb = CEBClass(f_c=f_c)
        E = ceb.E
        nu_value = Theory.nu(f_c)
        return E / (2*(1+nu_value))

    @staticmethod
    def K(f_c):
        """
        Calculate bulk modulus K from characteristic compressive strength.
        Parameters:
        -----------
        f_c : float
            Characteristic compressive strength of concrete (MPa)
        Returns:
        --------
        float
            Bulk modulus K (MPa)
        """ 
        from CEB import CEBClass
        ceb = CEBClass(f_c=f_c)
        E = ceb.E
        nu_value = Theory.nu(f_c)
        return E / (3*(1-2*nu_value)) 

    @staticmethod
    def nu(f_c):
        """
        Calculate Poisson's ratio from characteristic compressive strength.

        According to CEB-FIP Model Code 1990 (5.1.7.3 Poisson's ratio), the Poisson's 
        ratio is constant for the characteristic compressive strength of concrete
        (f_ck) in the range -0.6*f_ck < sigma < 0.8*f_ctk, where f_ck is the      
        characteristic compressive strength of concrete (f_c) is equal to 0.2.
        
        Parameters:
        -----------
        f_c : float
            Characteristic compressive strength of concrete (MPa)
        Returns:
        --------
        float
            Poisson's ratio (nu)
        """
        return 0.2    

    @staticmethod
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

    @staticmethod
    def sigma_m(sigma_1, sigma_2, sigma_3):
        """
        Calculate mean stress (hydrostatic stress).
        
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
            Mean stress
        """
        return Theory.I_1(sigma_1, sigma_2, sigma_3) / 3.0

    @staticmethod
    def S_1(sigma_1, sigma_2, sigma_3):
        """
        Calculate first stress deviator component.
        
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
            First stress deviator component
        """
        return sigma_1 - Theory.sigma_m(sigma_1, sigma_2, sigma_3)

    @staticmethod
    def S_2(sigma_1, sigma_2, sigma_3):
        """
        Calculate second stress deviator component.
        
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
            Second stress deviator component
        """
        return sigma_2 - Theory.sigma_m(sigma_1, sigma_2, sigma_3)

    @staticmethod
    def S_3(sigma_1, sigma_2, sigma_3):
        """
        Calculate third stress deviator component.
        
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
            Third stress deviator component
        """
        return sigma_3 - Theory.sigma_m(sigma_1, sigma_2, sigma_3)

    @staticmethod
    def J_2(sigma_1, sigma_2, sigma_3):
        """
        Calculate second stress invariant J2.
        
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
        return 0.5 * (Theory.S_1(sigma_1, sigma_2, sigma_3)**2 + 
                      Theory.S_2(sigma_1, sigma_2, sigma_3)**2 + 
                      Theory.S_3(sigma_1, sigma_2, sigma_3)**2)


# Backward compatibility: expose functions at module level
G = Theory.G
K = Theory.K
nu = Theory.nu
I_1 = Theory.I_1
sigma_m = Theory.sigma_m
S_1 = Theory.S_1
S_2 = Theory.S_2
S_3 = Theory.S_3
J_2 = Theory.J_2