import numpy as np
from theory import G, K, nu

def DIF_c(f_c):
    f_co = 10
    f_cs = f_c
    strainRateStatic = 30.0E-6
    strainRateMax    = 300
    strainRateCutoff = 30
    #
    alpha_s = 1.0/(5.0+9.0*(f_cs/f_co))
    beta_s = pow(10, 6.0*alpha_s-2)
    #
    strainRateLow = np.linspace(strainRateStatic, strainRateCutoff, strainRateCutoff)
    DIFLow = pow(strainRateLow/strainRateStatic, alpha_s)
    #
    strainRateHigh = np.linspace(strainRateCutoff, strainRateMax, strainRateMax-strainRateCutoff )
    DIFHigh = beta_s*pow(strainRateHigh/strainRateStatic, 1.0/3.0)
    #
    strainRate = np.concatenate((strainRateLow, strainRateHigh))
    DIF = np.concatenate((DIFLow, DIFHigh))
    #
    DIFCurve = np.vstack((strainRate, DIF))
    #DIFCurve = np.vstack((strainRateLow, DIFLow))
    #
    return  DIFCurve

def DIF_t(f_c):
    f_co = 10
    f_cs = f_c
    strainRateStatic = 3.0E-6
    strainRateMax    = 300
    strainRateCutoff = 30
    #
    delta_s = 1.0/(10.0+6.0*f_cs/f_co)
    beta_s  = pow(10, 7.11*delta_s-2.33)
    #
    strainRateLow = np.linspace(strainRateStatic, strainRateCutoff, strainRateCutoff)
    DIFLow = pow(strainRateLow/strainRateStatic, 1.016*delta_s)
    #
    strainRateHigh = np.linspace(strainRateCutoff, strainRateMax, (strainRateMax-strainRateCutoff))
    DIFHigh = beta_s*pow(strainRateHigh/strainRateStatic, 1.0/3.0)
    #
    strainRate = np.concatenate((strainRateLow, strainRateHigh))
    DIF = np.concatenate((DIFLow, DIFHigh))
    #
    DIFCurve = np.vstack((strainRate, DIF))   
    return DIFCurve  

def sigma_elastic(f_c, strain):
    """
    Calculate elastic stress using Hooke's law with elastic modulus from CEB data
    
    Parameters:
    f_c : float
        Characteristic compressive strength of concrete (MPa)
    strain : float or array-like
        Strain values
    d_max : float, optional
        Maximum aggregate size (mm) (default: 16.0)
    delta_f : float, optional
        Difference between mean and characteristic strength (default: 8.0 MPa)
        
    Returns:
    float or array-like
        Elastic stress values (sigma_elastic = strain * E)
    """
    # Get CEB data including elastic modulus
    E = CEB(f_c=f_c)['E']
    
    return strain * E

def CEB(f_c = 40, d_max = 16.0, rho = 2.4E-9, curve_array_size = 100, delta_f = 8.):
    ################################################
    # 5.1.4 Compressive strength The
    ################################################

    # specific characteristic compressive strength 
    f_ck = f_c
    
    # mean compressive strength
    f_cm = f_ck + delta_f 

    # biaxial compression strength, MPa
    f_bc     = 1.15*f_ck
    
    ################################################
    # 5.1.5 Tensile strength and fracture properties
    ################################################
    # 5.1.5.1 Tensile strength
    ################################################
    
    # mean value of tensile strenght
    if f_ck <= 50: 
        f_ctm = 0.3*pow(f_ck,2./3.)
    else:
        f_ctm = 2.12*np.log(1+0.1*(f_ck+delta_f))

    # lower bounds for characteristic tensile strenght
    f_ck_min = 0.7*f_ctm
    
    # upper bounds for characteristic tensile strenght
    f_ck_max = 1.3*f_ctm
    
    # uniaxial tensile strenght
    f_t = f_ctm
    
    # biaxial tensile strength
    f_bt = f_t
    # triaxial tensile strength
    f_tt = f_t
    
    ################################################
    # 5.1.5.2 Fracture energy
    ################################################
    
    G_f_2010 = 73*pow(f_cm,0.18) # fracture energy 2010
    
    # MPa
    f_cm0 = 10.0                                  
    
    # Base value for fracture energy, Nmm/mm^2
    G_f0 = 0.021+5.357E-4*d_max
    
    # Fracture energy, Nmm/mm^2
    G_f  = G_f0*pow(f_cm/f_cm0, 0.7)
    G_ft = G_f
    G_fc = G_ft*100
    G_fs = G_ft
    
    ################################################
    # 5.1.7 Modulus of elasticity and Poisson’s ratio
    ################################################
    # 5.1.7.2 Modulus of elasticity
    ################################################
    
    # MPa
    E_c0 = 21.5E+3
        
    # aggregate qualititive values
    alpha_E = 1.0
    
    # Elacticity modulud at 28 day
    E_ci = E_c0*alpha_E*pow((f_ck+delta_f)/f_cm0,1./3.) 
    
    alpha_i = 0.8+0.2*f_cm/88
    if alpha_i > 1.0: 
        alpha_i = 1.0
        
    # Reduced elasticity modulus 
    E_c = alpha_i*E_ci                               
    E = E_ci
    
    
    
    ################################################
    # 5.1.8 Stress-strain relations for short-term loading
    ################################################
    # 5.1.8.1 Compression
    ################################################
    
    # Strain coressponding to f_cm
    # Table 3.1 in Eurocode2 
    epsilon_c1 = -0.7*pow(f_cm,0.31)
    if epsilon_c1 > 2.8: 
        epsilon_c1 = 2.8/1000.
    else: 
        epsilon_c1 /=1000.
     
    # secan modulus from the origin to the peak compressive stress f_cm
    E_c1=f_cm/abs(epsilon_c1)
        
    # plasticity number
    k = E_ci/E_c1
     
    # ascending brunch before epsilon_c_lim
    epsilon_c_lim  = 0.25*pow(0.5*k+1,2)-0.5
    epsilon_c_lim  = pow(epsilon_c_lim, 0.5)
    epsilon_c_lim += 0.5*(0.5*k+1)
    epsilon_c_lim *= epsilon_c1
    
    epsilon_c = np.linspace(epsilon_c_lim, 0, int(curve_array_size/2))
    
    # relative strain for curve 
    eta=epsilon_c/epsilon_c1
    
    sigma_c = (k*eta-pow(eta,2))
    sigma_c /= (1+(k-2)*eta)
    sigma_c *= -f_cm
    
    x = epsilon_c
    y = sigma_c
    
    # descending brunch after epsilon_c_lim
    epsilon_c = np.linspace(epsilon_c_lim*5.0, epsilon_c_lim, int(curve_array_size/2))
    
    eta_1 = epsilon_c/epsilon_c1
    eta_2 = epsilon_c_lim/epsilon_c1
    
    xi  = pow(eta_2,2)*(k-2)
    xi += 2*eta_2-k
    xi /= pow(eta_2*(k-2)+1,2)
    xi *= 4.0
    
    a = 1.0/eta_2
    
    sigma_c  = xi/eta_2-2.0/pow(eta_2,2)
    sigma_c *= pow(eta_1,2)
    sigma_c += (4/eta_2-xi)*eta_1
    sigma_c  = -f_cm/sigma_c
    
    epsilon_c = np.concatenate((epsilon_c,x))
    sigma_c = np.concatenate((sigma_c,y))
    
  
    ################################################
    # 5.1.8.2 Tension
    ################################################
    # MPa
    # max tensile strain
    epsilon_ct_max = 0.15/1000

    # tensile strain array
    epsilon_ct = np.linspace(0, epsilon_ct_max , curve_array_size)
    sigma_ct = np.zeros(curve_array_size) 

    sigma_ct_low   = E_ci*epsilon_ct
    sigma_ct_high  = 0.00015-epsilon_ct
    sigma_ct_high /= 0.00015-0.9*f_ctm/E_ci
    sigma_ct_high  = f_ctm*(1-0.1*sigma_ct_high)

    border = 0.9*f_ctm

    for i, sigma_i in enumerate(sigma_ct_low):
        if sigma_i <= border:
            sigma_ct[i] = sigma_i
        else:
            sigma_ct[i] = sigma_ct_high[i]
   
    # crack opening
    w_1 = G_f/f_ctm
    w_c = 5.0*G_f/f_ctm
    
    w_crack1 = np.linspace(0, w_1, int(curve_array_size/2))
    sigma_ct_crack1 = f_ctm*(1.00-0.80*w_crack1/w_1)
    
    w_crack2 = np.linspace(w_1, w_c, int(curve_array_size/2))
    sigma_ct_crack2 = f_ctm*(0.25-0.05*w_crack2/w_1)
    
    w = np.concatenate((w_crack1, w_crack2))
    sigma_ct_crack = np.concatenate((sigma_ct_crack1, sigma_ct_crack2))
        
    ################################################
    # MAT_CONCRETE_DAMAGE_PLASTIC_MODEL stecial data
    # Tensile softening branch for exponential tensile damage formulation
    G_f = G_ft
    WF = G_f/f_t
    # ksi = ft*(fbc**2-fc**2)/(fbc*(fc**2-ft**2))
    # ECC = (1+ksi)/(1-ksi)
    
    ################################################
    # Record data from CEB-FIB estimations
    data = {}
    data['f_c']   = f_c  
    data['f_cm0'] = f_cm0  
    data['f_cm']  = f_cm 
    data['f_cm']  = f_cm   
    data['f_t']   = f_t 
    data['f_ctm'] = f_ctm
    data['f_tt']  = f_tt     
    data['f_bc']  = f_bc 
    data['G_fc']  = G_fc
    data['G_ft']  = G_ft     
    data['G_fs']  = G_fs     
    data['d_max'] = d_max
    data['rho']   = rho 
    data['nu']    = nu(f_c)     
    data['E']     = E 
    data['E_ci']  = E_ci
    data['E_c1']  = E_c1
    data['G']     = E / (2*(1+nu(f_c)))       
    data['K']     = E / (3*(1-2*nu(f_c))) 
    data['WF']    = WF
    data['epsilon_c1'] = epsilon_c1
    data['k']     = k
    data['compression_curve']   = np.vstack((epsilon_c, sigma_c))
    data['tension_curve']       = np.vstack((epsilon_ct, sigma_ct))
    data['crack_opening_curve'] = np.vstack((w, sigma_ct_crack))
    #data['ECC']  = ECC      
    return data