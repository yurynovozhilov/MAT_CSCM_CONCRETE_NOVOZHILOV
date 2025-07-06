import numpy as np
from CEB import *

def P(f_c, A_p,B_p,C_p):
    return A_p*pow(f_c,2)+B_p*f_c+C_p

##############################################################
# Concrete yield function 
##############################################################
def F_f(f_c, I, rev):
    # Shear surface F_f is defined along 
    # the compression meridian TXC
    result  = alpha(f_c,rev)
    result -= lamda(f_c,rev)*np.exp(-beta(f_c,rev)*I)
    result += theta(f_c,rev)*I
    return result

def L(kappa, kappa_0):
    # L(kappa) is the position on the I-axis where 
    # the ellipse (cap surface) intersects 
    # the shear failure surface
    #
    # kappa_0 is the value of I at the initial intersection 
    # of the cap and shear surfaces before hardening 
    # is engaged (before the cap moves).  
    if kappa > kappa_0:
        return kappa
    else:
        return kappa_0
def X(f_c, I, kappa, kappa_0, rev):
    # X(kappa) is the position on the I-axis where the outer
    # edge of the ellipse (cap surface) intersects
    return L(kappa, kappa_0)+R(f_c, rev)*F_f(f_c, L(kappa, kappa_0), rev)

def F_c(f_c, I, kappa, kappa_0, rev):
    # Cap failure surface function F_c
    # kappa is a hardening parameter that causes the cap 
    # surface to move (expand or contract) 
    result  = (I-L(kappa, kappa_0))
    result *= (abs(result)+result)
    
#   result /= (2*pow( X(f_c, I, kappa, kappa_0, rev)-L(kappa, kappa_0),2))
    result /= (2*pow(X0(f_c,rev=3),2))
    result  = 1 - result
    for i, value in enumerate(result):
        if value < 0:
            result[i] = 0
    return result

def Rubin(f_c, I, rev, resolution=30):

    beta_hat = np.linspace(-np.pi/6.0, np.pi , resolution)

    q1  = Q_1(f_c, I, rev)
    q2  = Q_2(f_c, I, rev)

    a_0 = 2*pow(q1,2)*(q2-1)
    a_1 = np.sqrt(3)*q2+2*q1*(q2-1)
    a_2 = q2
    a   = (-a_1+np.sqrt(pow(a_1,2)-4*a_2*a_0))/(2*a_2)

    b   = pow(2*q1+a,2)-3
    b_0 = -(3+b-pow(a,2))/4
    b_1 = a*(np.cos(beta_hat)-a*np.sin(beta_hat))
    b_2 = pow(np.cos(beta_hat)-a*np.sin(beta_hat),2)+b*pow(np.sin(beta_hat),2)

    RScale = (-b_1+np.sqrt(pow(b_1,2)-4*b_2*b_0))/(2*b_2)
    
    RCurve = np.vstack((beta_hat, RScale))
    return RCurve

##############################################################
# Parameters for the compressive meridian (TXC)
##############################################################
def alpha(f_c,rev=3):
    if rev   == 1: return P(f_c, -0.003, 0.3169747, 7.7047)
    elif rev == 2: return 13.9846*np.exp(f_c/68.8756)-13.8981
    elif rev == 3: return 2.5801E-03*pow(f_c,2)+1.6405E-01*f_c+4.3506E-01
    else: return False 

def lamda(f_c,rev=3):
    if   rev == 1: return P(f_c, 0.0, 0.0, 10.5)
    elif rev == 2: return 3.6657*np.exp(f_c/39.9363)-4.7092
    elif rev == 3: return 3.0220E-03*pow(f_c,2.0231E+00)
    else: return False 
    
def beta(f_c,rev=3):
    if rev   == 1: return P(f_c, 0.0, 0.0, 1.929E-02)
    elif rev == 2: return 18.17791*pow(f_c,-1.7163)
    elif rev == 3: return 1.2317E+01*pow(f_c,-1.5974E+00)
    else: return False 
    
def theta(f_c,rev=3):
    if   rev == 1: return P(f_c, 1.3216E-05, 2.3548E-03, 0.2140058)
    elif rev == 2: return 0.3533-3.3294E-4*f_c-3.8182E-6*pow(f_c,2)
    elif rev == 3: return -3.4286E-06*pow(f_c,2)-3.7971E-04*f_c+3.5436E-01
    else: return False 
    
def TXC(f_c, I, rev):
    return F_f(f_c, I, rev)

##############################################################
# Parameters for the shear meridian (TOR)
##############################################################

def alpha_1(f_c,rev=3):
    if rev   == 1: return P(f_c, 0, 0, 0.74735)
    elif rev == 2: return 0.82
    elif rev == 3: return 1/np.sqrt(3.0)+lamda_1(f_c,rev)
    else: return False 
    
def lamda_1(f_c,rev=3):
    if   rev == 1: return P(f_c, 0, 0, 0.17)
    elif rev == 2: return 0.2407
    #elif rev == 3: return round(alpha_1(f_c, rev)-1/sqrt(3.0), 4)
    elif rev == 3: return -2.0833E-07*pow(f_c,3) + 3.7571E-05*pow(f_c,2) - 2.3049E-03*f_c + 2.8860E-01
    else: return False 
    
def beta_1(f_c,rev=3):
    if rev   == 1: return P(f_c, -1.9972e-05, 2.2655e-04, 8.1748e-02)
    elif rev == 2: return 0.33565*pow(f_c,-0.95383)
    elif rev == 3: return 3.4093E-01*pow(f_c,-9.4944E-01)
    else: return False 
    
def theta_1(f_c,rev=3):
    if   rev == 1: return P(f_c, -4.0856E-07, -1.2132E-06, 1.5593E-03)
    elif rev == 2: return 0
    elif rev == 3: return 0
    else: return False 
    
def Q_1(f_c, I, rev=3): 
    if type(I) != np.ndarray:
        I = np.array([I])
    for i, value in enumerate(I):
        if value >= 0:
            # TOR/TXC strength ratio
            return alpha_1(f_c,rev)-lamda_1(f_c,rev)*np.exp(-beta_1(f_c,rev)*i)+theta_1(f_c,rev)*i
        else:
            # Values to simulate a triangular yield surface 
            # in the deviatoric plane fro tensile pressure
            return 1/np.sqrt(3.0)

def TOR(f_c, I, rev=1):
    # Q_1 = 1/sqrt(3) for tension load (I<=0)
    I_tension     = I[I<=0]
    I_compression = I[I> 0]
    result_negative    =           1.0/np.sqrt(3.0)*TXC(f_c,I_tension,rev)
    result_compression = Q_1(f_c,I_compression,rev)*TXC(f_c,I_compression,rev)
    return np.hstack((result_negative,result_compression))

##############################################################
# Parameters for tensile meridian (TXE)
##############################################################

def alpha_2(f_c,rev=3):
    if rev   == 1: return P(f_c, 0, 0, 0.66)
    elif rev == 2: return 0.76
    elif rev == 3: return round(0.5+lamda_2(f_c,rev), 4)
    else: return False 

def lamda_2(f_c,rev=3):
    if   rev == 1: return P(f_c, 0, 0, 0.16)
    elif rev == 2: return 0.26
    elif rev == 3: return 3.0029E-01*pow(f_c,-4.2269E-02)
    else: return False 
    
def beta_2(f_c,rev=3):
    if rev   == 1: return P(f_c, -1.9972e-05, 2.2655e-04, 8.2748e-02)
    elif rev == 2: return 0.285*pow(f_c,-0.94843)
    elif rev == 3: return 2.8898E-01*pow(f_c,-9.4776E-01)
    else: return False 
    
def theta_2(f_c,rev=3):
    if   rev == 1: return P(f_c, -4.8697e-07, -1.8883e-06, 1.8822e-03)
    elif rev == 2: return 0
    elif rev == 3: return 0
    else: return False 
    
def Q_2(f_c, I, rev=1):
    if type(I) != np.ndarray:
        I = np.array([I])
    for i, value in enumerate(I):
        if i >= 0:
            # TXE/TXC strength ratio
            return alpha_2(f_c,rev)-lamda_2(f_c,rev)*np.exp(-beta_2(f_c,rev)*i)+theta_2(f_c,rev)*i
        else:
            # Values to simulate a triangular yield surface 
            # in the deviatoric plane fro tensile pressure
            return 0.5

def TXE(f_c, I, rev=1):
    # Q_2 = 0.5 for tension load (I<=0)
    I_tension     = I[I<=0]
    I_compression = I[I> 0]
    result_negative    =                        0.5*TXC(f_c,I_tension,rev)
    result_compression = Q_2(f_c,I_compression,rev)*TXC(f_c,I_compression,rev)
    return np.hstack((result_negative,result_compression))

##############################################################
# CAP surface parameters
##############################################################
def X0(f_c,rev=3):
    #  the initial location of the cap when kappa = kappa_0
    if rev   == 1: return P(f_c, 8.769178e-03, -7.3302306e-02, 84.85)
    elif rev == 2: return 17.087+1.892*f_c
    elif rev == 3: return 4.0224E+00*f_c - 7.0784E+01
    else: return False
    
def R(f_c,rev=3):
    # ellipticity ratio - the ratio of major to minor ellipce axes
    if rev   == 1: return 5
    elif rev == 2: return 4.45994*np.exp(-f_c/11.51679)+1.95358
    elif rev == 3: return 5.0000E-04*pow(f_c,2)-5.9000E-02*f_c+3.6600E+00
    else: return False 
    
def W(f_c,rev=3):
    # the maximum plastic volume strain
    '''
    The maximum plastic volume change sets the range in volumetric strain over 
    which the pressure-volumetric strain curve is nonlinear (from onset to lock-up). 
    Typically, the maximum plastic volume change is approximately equal 
    to the porosity of the air voids. A value of 0.05 indicates an air void 
    porosity of 5 percent. 
    '''
    if rev   == 1: return 0.05
    elif rev == 2: return 0.065
    elif rev == 3: return 0.065
    else: return False 

def D_1(f_c,rev=3):
    if rev   == 1: return 2.5E-4
    elif rev == 2: return 6.11e-4
    elif rev == 3: return 6.11e-4
    else: return False 
    
def D_2(f_c,rev=3):
    if rev   == 1: return 3.49E-7
    elif rev == 2: return 2.225E-6
    elif rev == 3: return 2.225E-6
    else: return False 
    
def epsilon_v_p(f_c,X,rev=1):
    # plastic volume strain - based for motion (expansion and contraction) of the cap
    return W(f_c,rev)*(1-np.exp(-D_1(f_c,rev)*(X-X0(f_c,rev))-D_2(f_c,rev)*pow(X-X0(f_c,rev),2)))

def hydrostaticCompressionParameters(f_c,X,rev=1):
    return D_1(f_c,rev)*(X-X0(f_c,rev))+D_2(f_c,rev)*pow(X-X0(f_c,rev),2)

##############################################################
# Damage
##############################################################
def B(f_c, E, G_f_c, l ,rev=1):
    # Ductile shape softening parameter
    if rev   == 1: 
        return 100
    elif rev == 2: 
        bfit  = 2.0*G_f_c/l
        bfit += f_c*2/E
        bfit  = pow(bfit, 0.5)
        bfit += f_c/pow(E,0.5)
        bfit /= G_f_c/l
        return bfit
    else: 
        return False 
    
def D(f_t, E, G_ft, l, rev=1):
    # Brittle shape softening parameter
    if rev   == 1: 
        return 0.1
    elif rev == 2: 
        return l*f_t/(G_ft*pow(E, 0.5))
    else: 
        return False 
    
def pmod():
    # Modify moderate pressure softening parameter
    '''
    In addition to reducing the maximum damage level with confinement (pressure), 
    the compressive softening parameter, A, may also be reduced with confinement.

    A *= pow((d_max+0.001),pmod)

    Here pmod is a user-specified input parameter. Its default value is 0.0. 
    Input compression value of pmod reduces A when the maximum damage is less than 0.999; 
    otherwise A is unaffected by pmod. Thus, it is only active at moderate confinement levels.
    '''
    return 0.0

def brittleDamage(tau_b):
    d  = (1+D)
    d /= (1+D*np.exp(-C*(tau_b-r_0b)))
    d -= 1
    d *= d_max/D
    return d

def ductileDamage(tau_d):
    d  = (1+B)
    d /= (1+B*np.exp(-a*(tau_d-r_0d)))
    d -= 1
    d *= d_max/B
    return d
          
def A():
    b = -2*(1+B)*log(1+B)*L*tau_0_Ductile
    c = -2*L*(1+B)*dilog/G_f_Ductile
    A = (-b+np.sqrt(pow(b,2)-4*c))*0.5
    return A
          
def C():
    return r_0b*L*(1+D)/(G_f*D)*log(1+D)

############################################################## 
# Strain rate
##############################################################

def n_t(f_c,rev=1): 
    if rev   == 1: return 0.48
    elif rev == 2: return 0
    else: return False 
    
def eta_0_t(f_c,rev=1): 
    f_c_in_psi= f_c*145.0377
    if rev   == 1: return P(f_c_in_psi, 8.0614774E-13, -9.77736719E-10, 5.0752351E-05)
    elif rev == 2: return 0
    else: return False 
          
def eta_t(f_c,strainRate,rev):
    # fluidity parameter in uniaxial tensile stress
    return eta_0_t(f_c,rev)/pow(strainRate,n_t(f_c,rev))
    
def n_c(f_c,rev=1): 
    if rev   == 1: return 0.78
    elif rev == 2: return 0
    else: return False 
    
def eta_0_c(f_c,rev=1):
    f_c_in_psi= f_c*145.0377
    if rev   == 1: return P(f_c_in_psi, 1.2772337E-11, -1.0613722E-07, 3.203497E-4)
    elif rev == 2: return 0
    else: return False
          
def eta_c(f_c,strainRate,rev):
    # fluidity parameter in uniaxial compressive stress
    return eta_0_c(f_c,rev)/pow(strainRate,n_c(f_c,rev))

def eta_s(f_c,rev):
    # fluidity parameter in shear stress
    return Srate(f_c,rev)*eta_t(f_c,rev)

def Srate(f_c, rev):
    # ratio of effective shear stress to tensile stress fluidity parameters
    return 1.0
      
def overt(f_c,rev=1): 
    return P(f_c, 1.309663E-02, -0.3927659, 21.45)    

def overc(f_c,rev=1): 
    return overt(f_c,rev=1)    
         
def DIFCSCM_t(f_c, rev=1, strainRateMax = 1000):
    data = CEB(f_c)
    f_t  = data['f_t']
    E    = data['E']
    overTension = overt(f_c,rev)

    strainRateStatic = 30.0E-6
    strainRate = np.linspace(strainRateStatic, strainRateMax, strainRateMax)

    inviscidStrengths     = f_t
    viscoplasticStrengths = E*strainRate*eta_t(f_c,strainRate,rev)

    for i, strengths in enumerate(viscoplasticStrengths):
        if strengths > overTension:
            viscoplasticStrengths[i] = overTension

    DIF = viscoplasticStrengths/inviscidStrengths+1
    DIFCurve = np.vstack((strainRate, DIF))
    return DIFCurve
          
def DIFCSCM_c(f_c, rev=1, strainRateMax = 1000):
    data = CEB(f_c)
    E    = data['E']
    overCompression = overc(f_c,rev)

    strainRateStatic = 30.0E-6
    strainRate = np.linspace(strainRateStatic, strainRateMax, strainRateMax)

    inviscidStrengths     = f_c
    viscoplasticStrengths = E*strainRate*eta_c(f_c,strainRate,rev)

    for i, strengths in enumerate(viscoplasticStrengths):
        if strengths > overCompression:
            viscoplasticStrengths[i] = overCompression
    #
    DIF = viscoplasticStrengths/inviscidStrengths+1
    DIFCurve = np.vstack((strainRate, DIF))
    return DIFCurve


