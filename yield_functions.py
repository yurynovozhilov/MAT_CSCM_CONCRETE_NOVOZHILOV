"""
Yield Surface Functions for CSCM Model

This module contains specialized yield surface functions used in the Continuous Surface Cap Model (CSCM)
for concrete material behavior simulation. These functions implement various yield criteria and 
stress invariant relationships.

References:
-----------
- Murray, Y.D., Abu-Odeh, A., Bligh, R. (2007). Evaluation of LS-DYNA Concrete Material Model 159. 
  Federal Highway Administration Report FHWA-HRT-05-063.
- Malvar, L.J., Crawford, J.E., Wesevich, J.W., Simons, D. (1997). A plasticity concrete material 
  model for DYNA3D. International Journal of Impact Engineering, 19(9-10), 847-873.
- Willam, K.J., Warnke, E.P. (1975). Constitutive model for the triaxial behavior of concrete. 
  Proceedings, International Association for Bridge and Structural Engineering, Vol. 19, Zurich.
"""

import numpy as np
from MatCSCM import Revision


def Q1MC(mat, I, rev=Revision.REV_1):
    """
    Mohr-Coulomb yield function Q1 parameter.
    
    This function calculates the Q1 parameter for the Mohr-Coulomb yield criterion,
    which relates the deviatoric stress to the hydrostatic stress in the meridional plane.
    
    Mathematical expression:
    Q1MC = √3 * Q2 / (1 + Q2)
    
    Where Q2 is the ratio of tensile to compressive meridians.
    
    Parameters:
    -----------
    mat : MatCSCM
        Material object containing CSCM parameters
    I : float or array-like
        First stress invariant (hydrostatic stress)
    rev : Revision
        CSCM model revision number
        
    Returns:
    --------
    float or array-like
        Q1MC parameter value(s)
        
    References:
    -----------
    Murray, Y.D. et al. (2007), Equation for Mohr-Coulomb yield criterion
    """
    q2 = mat.evaluate.Q_2(I, rev)
    return np.sqrt(3) * q2 / (1 + q2)


def Q2MC(mat, I, rev=Revision.REV_1):
    """
    Mohr-Coulomb yield function Q2 parameter.
    
    This function calculates the Q2 parameter for the Mohr-Coulomb yield criterion,
    representing the ratio of tensile to compressive meridian strengths.
    
    Mathematical expression:
    Q2MC = TXE / TXC
    
    Where:
    - TXE = Tensile meridian strength
    - TXC = Compressive meridian strength
    
    Parameters:
    -----------
    mat : MatCSCM
        Material object containing CSCM parameters
    I : float or array-like
        First stress invariant (hydrostatic stress)
    rev : Revision
        CSCM model revision number
        
    Returns:
    --------
    float or array-like
        Q2MC parameter value(s)
        
    References:
    -----------
    Murray, Y.D. et al. (2007), Equation for meridian ratio in Mohr-Coulomb criterion
    """
    return mat.evaluate.TXE(I, rev) / mat.initialize.TXC(I, rev)


def Q1WW(mat, I, rev=Revision.REV_1):
    """
    Willam-Warnke yield function Q1 parameter.
    
    This function calculates the Q1 parameter for the Willam-Warnke yield criterion,
    which provides a more sophisticated representation of concrete behavior under
    multiaxial stress states compared to the Mohr-Coulomb criterion.
    
    Mathematical expression:
    Q1WW = (√3 * q + (2*Q2 - 1) * √(3*q + 5*Q2² - 4*Q2)) / (3*q + (1 - 2*Q2)²)
    
    Where:
    - q = 1 - Q2²
    - Q2 = ratio of tensile to compressive meridians
    
    Parameters:
    -----------
    mat : MatCSCM
        Material object containing CSCM parameters
    I : float or array-like
        First stress invariant (hydrostatic stress)
    rev : Revision
        CSCM model revision number
        
    Returns:
    --------
    float or array-like
        Q1WW parameter value(s)
        
    References:
    -----------
    Willam, K.J., Warnke, E.P. (1975), Constitutive model for the triaxial behavior of concrete
    Murray, Y.D. et al. (2007), Implementation of Willam-Warnke yield criterion in CSCM
    """
    q2 = mat.evaluate.Q_2(I, rev)
    q = 1 - pow(q2, 2)
    
    numerator = (np.sqrt(3) * q + 
                (2 * q2 - 1) * np.sqrt(3 * q + 5 * pow(q2, 2) - 4 * q2))
    denominator = 3 * q + pow(1 - 2 * q2, 2)
    
    return numerator / denominator


def TORMC(mat, I, rev=Revision.REV_1):
    """
    Mohr-Coulomb torsional strength.
    
    This function calculates the torsional strength based on the Mohr-Coulomb yield criterion.
    
    Mathematical expression:
    TORMC = Q1MC * TXC
    
    Where:
    - Q1MC = Mohr-Coulomb Q1 parameter
    - TXC = Compressive meridian strength
    
    Parameters:
    -----------
    mat : MatCSCM
        Material object containing CSCM parameters
    I : float or array-like
        First stress invariant (hydrostatic stress)
    rev : Revision
        CSCM model revision number
        
    Returns:
    --------
    float or array-like
        Torsional strength value(s) based on Mohr-Coulomb criterion
        
    References:
    -----------
    Murray, Y.D. et al. (2007), Torsional strength calculation for Mohr-Coulomb criterion
    """
    return Q1MC(mat, I, rev) * mat.initialize.TXC(I, rev)


def TXEMC(mat, I, rev=Revision.REV_1):
    """
    Mohr-Coulomb tensile meridian strength.
    
    This function calculates the tensile meridian strength based on the Mohr-Coulomb yield criterion.
    
    Mathematical expression:
    TXEMC = Q2MC * TXC
    
    Where:
    - Q2MC = Mohr-Coulomb Q2 parameter
    - TXC = Compressive meridian strength
    
    Parameters:
    -----------
    mat : MatCSCM
        Material object containing CSCM parameters
    I : float or array-like
        First stress invariant (hydrostatic stress)
    rev : Revision
        CSCM model revision number
        
    Returns:
    --------
    float or array-like
        Tensile meridian strength value(s) based on Mohr-Coulomb criterion
        
    References:
    -----------
    Murray, Y.D. et al. (2007), Tensile meridian strength for Mohr-Coulomb criterion
    """
    return Q2MC(mat, I, rev) * mat.initialize.TXC(I, rev)


def TORWW(mat, I, rev=Revision.REV_1):
    """
    Willam-Warnke torsional strength.
    
    This function calculates the torsional strength based on the Willam-Warnke yield criterion.
    
    Mathematical expression:
    TORWW = Q1WW * TXC
    
    Where:
    - Q1WW = Willam-Warnke Q1 parameter
    - TXC = Compressive meridian strength
    
    Parameters:
    -----------
    mat : MatCSCM
        Material object containing CSCM parameters
    I : float or array-like
        First stress invariant (hydrostatic stress)
    rev : Revision
        CSCM model revision number
        
    Returns:
    --------
    float or array-like
        Torsional strength value(s) based on Willam-Warnke criterion
        
    References:
    -----------
    Willam, K.J., Warnke, E.P. (1975), Constitutive model for the triaxial behavior of concrete
    Murray, Y.D. et al. (2007), Torsional strength calculation for Willam-Warnke criterion
    """
    return Q1WW(mat, I, rev) * mat.initialize.TXC(I, rev)


# Backward compatibility functions (using old naming convention)
def Q1MC_legacy(fc, rev=1):
    """
    Legacy Mohr-Coulomb Q1 function (backward compatibility).
    
    Note: This function is deprecated. Use Q1MC with MatCSCM object instead.
    """
    from MatCSCM import MatCSCM
    mat = MatCSCM(f_c=fc)
    return Q1MC(mat, 0, Revision(rev))


def Q2MC_legacy(fc, rev=1):
    """
    Legacy Mohr-Coulomb Q2 function (backward compatibility).
    
    Note: This function is deprecated. Use Q2MC with MatCSCM object instead.
    """
    from MatCSCM import MatCSCM
    mat = MatCSCM(f_c=fc)
    return Q2MC(mat, 0, Revision(rev))


def Q1WW_legacy(fc, rev=1):
    """
    Legacy Willam-Warnke Q1 function (backward compatibility).
    
    Note: This function is deprecated. Use Q1WW with MatCSCM object instead.
    """
    from MatCSCM import MatCSCM
    mat = MatCSCM(f_c=fc)
    return Q1WW(mat, 0, Revision(rev))