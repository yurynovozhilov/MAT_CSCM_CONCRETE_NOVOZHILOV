import numpy as np
from theory import G, K, nu


class CEBClass:
    """
    CEB-FIP Model Code implementation for concrete material properties.
    
    This class provides methods for calculating concrete material properties
    according to CEB-FIP Model Code standards, including strength parameters,
    elastic moduli, stress-strain curves, and fracture properties.
    """
    
    def __init__(self, f_c=40, d_max=16.0, rho=2.4E-9, curve_array_size=100, delta_f=8.):
        """
        Initialize CEB model with concrete parameters.
        
        Parameters:
        -----------
        f_c : float
            Characteristic compressive strength of concrete (MPa)
        d_max : float
            Maximum aggregate size (mm)
        rho : float
            Density (kg/mm^3)
        curve_array_size : int
            Number of points for stress-strain curves
        delta_f : float
            Difference between mean and characteristic strength (MPa)
        """
        self._f_c = f_c
        self._d_max = d_max
        self._rho = rho
        self._curve_array_size = curve_array_size
        self._delta_f = delta_f
        
        # Calculate all properties during initialization
        self._calculate_properties()
    
    def _calculate_properties(self):
        """Calculate all concrete properties based on input parameters."""
        ################################################
        # 5.1.4 Compressive strength The
        ################################################

        # specific characteristic compressive strength 
        f_ck = self._f_c
        
        # mean compressive strength
        f_cm = f_ck + self._delta_f 

        # biaxial compression strength, MPa
        f_bc = 1.15*f_ck
        
        ################################################
        # 5.1.5 Tensile strength and fracture properties
        ################################################
        # 5.1.5.1 Tensile strength
        ################################################
        
        # mean value of tensile strength
        if f_ck <= 50: 
            f_ctm = 0.3*pow(f_ck, 2./3.)
        else:
            f_ctm = 2.12*np.log(1+0.1*(f_ck+self._delta_f))

        # lower bounds for characteristic tensile strength
        f_ck_min = 0.7*f_ctm
        
        # upper bounds for characteristic tensile strength
        f_ck_max = 1.3*f_ctm
        
        # uniaxial tensile strength
        f_t = f_ctm
        
        # biaxial tensile strength
        f_bt = f_t
        # triaxial tensile strength
        f_tt = f_t
        
        ################################################
        # 5.1.5.2 Fracture energy
        ################################################
        
        G_f_2010 = 73*pow(f_cm, 0.18)  # fracture energy 2010
        
        # MPa
        f_cm0 = 10.0                                  
        
        # Base value for fracture energy, Nmm/mm^2
        G_f0 = 0.021+5.357E-4*self._d_max
        
        # Fracture energy, Nmm/mm^2
        G_f = G_f0*pow(f_cm/f_cm0, 0.7)
        G_ft = G_f
        G_fc = G_ft*100
        G_fs = G_ft
        
        ################################################
        # 5.1.7 Modulus of elasticity and Poisson's ratio
        ################################################
        # 5.1.7.2 Modulus of elasticity
        ################################################
        
        # MPa
        E_c0 = 21.5E+3
            
        # aggregate qualitative values
        alpha_E = 1.0
        
        # Elasticity modulus at 28 day
        E_ci = E_c0*alpha_E*pow((f_ck+self._delta_f)/f_cm0, 1./3.) 
        
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
        
        # Strain corresponding to f_cm
        # Table 3.1 in Eurocode2 
        epsilon_c1 = -0.7*pow(f_cm, 0.31)
        if epsilon_c1 > 2.8: 
            epsilon_c1 = 2.8/1000.
        else: 
            epsilon_c1 /= 1000.
         
        # secant modulus from the origin to the peak compressive stress f_cm
        E_c1 = f_cm/abs(epsilon_c1)
            
        # plasticity number
        k = E_ci/E_c1
         
        # ascending branch before epsilon_c_lim
        epsilon_c_lim = 0.25*pow(0.5*k+1, 2)-0.5
        epsilon_c_lim = pow(epsilon_c_lim, 0.5)
        epsilon_c_lim += 0.5*(0.5*k+1)
        epsilon_c_lim *= epsilon_c1
        
        epsilon_c = np.linspace(epsilon_c_lim, 0, int(self._curve_array_size/2))
        
        # relative strain for curve 
        eta = epsilon_c/epsilon_c1
        
        sigma_c = (k*eta-pow(eta, 2))
        sigma_c /= (1+(k-2)*eta)
        sigma_c *= -f_cm
        
        x = epsilon_c
        y = sigma_c
        
        # descending branch after epsilon_c_lim
        epsilon_c = np.linspace(epsilon_c_lim*5.0, epsilon_c_lim, int(self._curve_array_size/2))
        
        eta_1 = epsilon_c/epsilon_c1
        eta_2 = epsilon_c_lim/epsilon_c1
        
        xi = pow(eta_2, 2)*(k-2)
        xi += 2*eta_2-k
        xi /= pow(eta_2*(k-2)+1, 2)
        xi *= 4.0
        
        a = 1.0/eta_2
        
        sigma_c = xi/eta_2-2.0/pow(eta_2, 2)
        sigma_c *= pow(eta_1, 2)
        sigma_c += (4/eta_2-xi)*eta_1
        sigma_c = -f_cm/sigma_c
        
        epsilon_c = np.concatenate((epsilon_c, x))
        sigma_c = np.concatenate((sigma_c, y))
        
        ################################################
        # 5.1.8.2 Tension
        ################################################
        # MPa
        # max tensile strain
        epsilon_ct_max = 0.15/1000

        # tensile strain array
        epsilon_ct = np.linspace(0, epsilon_ct_max, self._curve_array_size)
        sigma_ct = np.zeros(self._curve_array_size) 

        sigma_ct_low = E_ci*epsilon_ct
        sigma_ct_high = 0.00015-epsilon_ct
        sigma_ct_high /= 0.00015-0.9*f_ctm/E_ci
        sigma_ct_high = f_ctm*(1-0.1*sigma_ct_high)

        border = 0.9*f_ctm

        for i, sigma_i in enumerate(sigma_ct_low):
            if sigma_i <= border:
                sigma_ct[i] = sigma_i
            else:
                sigma_ct[i] = sigma_ct_high[i]
       
        # crack opening
        w_1 = G_f/f_ctm
        w_c = 5.0*G_f/f_ctm
        
        w_crack1 = np.linspace(0, w_1, int(self._curve_array_size/2))
        sigma_ct_crack1 = f_ctm*(1.00-0.80*w_crack1/w_1)
        
        w_crack2 = np.linspace(w_1, w_c, int(self._curve_array_size/2))
        sigma_ct_crack2 = f_ctm*(0.25-0.05*w_crack2/w_1)
        
        w = np.concatenate((w_crack1, w_crack2))
        sigma_ct_crack = np.concatenate((sigma_ct_crack1, sigma_ct_crack2))
            
        ################################################
        # MAT_CONCRETE_DAMAGE_PLASTIC_MODEL special data
        # Tensile softening branch for exponential tensile damage formulation
        G_f = G_ft
        WF = G_f/f_t
        # ksi = ft*(fbc**2-fc**2)/(fbc*(fc**2-ft**2))
        # ECC = (1+ksi)/(1-ksi)
        
        # Store all calculated values as instance attributes
        self._f_cm0 = f_cm0
        self._f_cm = f_cm
        self._f_t = f_t
        self._f_ctm = f_ctm
        self._f_tt = f_tt
        self._f_bc = f_bc
        self._G_fc = G_fc
        self._G_ft = G_ft
        self._G_fs = G_fs
        self._E = E
        self._E_ci = E_ci
        self._E_c1 = E_c1
        self._WF = WF
        self._epsilon_c1 = epsilon_c1
        self._k = k
        self._compression_curve = np.vstack((epsilon_c, sigma_c))
        self._tension_curve = np.vstack((epsilon_ct, sigma_ct))
        self._crack_opening_curve = np.vstack((w, sigma_ct_crack))
    
    # Property methods for accessing calculated values
    @property
    def f_c(self):
        """Characteristic compressive strength (MPa)"""
        return self._f_c
    
    @property
    def f_cm0(self):
        """Reference mean compressive strength (MPa)"""
        return self._f_cm0
    
    @property
    def f_cm(self):
        """Mean compressive strength (MPa)"""
        return self._f_cm
    
    @property
    def f_t(self):
        """Uniaxial tensile strength (MPa)"""
        return self._f_t
    
    @property
    def f_ctm(self):
        """Mean tensile strength (MPa)"""
        return self._f_ctm
    
    @property
    def f_tt(self):
        """Triaxial tensile strength (MPa)"""
        return self._f_tt
    
    @property
    def f_bc(self):
        """Biaxial compression strength (MPa)"""
        return self._f_bc
    
    @property
    def G_fc(self):
        """Compressive fracture energy (Nmm/mm^2)"""
        return self._G_fc
    
    @property
    def G_ft(self):
        """Tensile fracture energy (Nmm/mm^2)"""
        return self._G_ft
    
    @property
    def G_fs(self):
        """Shear fracture energy (Nmm/mm^2)"""
        return self._G_fs
    
    @property
    def d_max(self):
        """Maximum aggregate size (mm)"""
        return self._d_max
    
    @property
    def rho(self):
        """Density (kg/mm^3)"""
        return self._rho
    
    @property
    def nu(self):
        """Poisson's ratio"""
        return nu(self._f_c)
    
    @property
    def E(self):
        """Elastic modulus (MPa)"""
        return self._E
    
    @property
    def E_ci(self):
        """Initial elastic modulus (MPa)"""
        return self._E_ci
    
    @property
    def E_c1(self):
        """Secant modulus to peak stress (MPa)"""
        return self._E_c1
    
    @property
    def G(self):
        """Shear modulus (MPa)"""
        return self._E / (2*(1+self.nu))
    
    @property
    def K(self):
        """Bulk modulus (MPa)"""
        return self._E / (3*(1-2*self.nu))
    
    @property
    def WF(self):
        """Tensile softening parameter"""
        return self._WF
    
    @property
    def epsilon_c1(self):
        """Strain at peak compressive stress"""
        return self._epsilon_c1
    
    @property
    def k(self):
        """Plasticity number"""
        return self._k
    
    @property
    def compression_curve(self):
        """Compression stress-strain curve"""
        return self._compression_curve
    
    @property
    def tension_curve(self):
        """Tension stress-strain curve"""
        return self._tension_curve
    
    @property
    def crack_opening_curve(self):
        """Crack opening curve"""
        return self._crack_opening_curve


def DIF_c(f_c):
    """
    Dynamic Increase Factor for compression.
    
    Parameters:
    -----------
    f_c : float
        Characteristic compressive strength of concrete (MPa)
        
    Returns:
    --------
    numpy.ndarray
        2D array with strain rates and corresponding DIF values
    """
    f_co = 10
    f_cs = f_c
    strainRateStatic = 30.0E-6
    strainRateMax = 300
    strainRateCutoff = 30
    #
    alpha_s = 1.0/(5.0+9.0*(f_cs/f_co))
    beta_s = pow(10, 6.0*alpha_s-2)
    #
    strainRateLow = np.linspace(strainRateStatic, strainRateCutoff, strainRateCutoff)
    DIFLow = pow(strainRateLow/strainRateStatic, alpha_s)
    #
    strainRateHigh = np.linspace(strainRateCutoff, strainRateMax, strainRateMax-strainRateCutoff)
    DIFHigh = beta_s*pow(strainRateHigh/strainRateStatic, 1.0/3.0)
    #
    strainRate = np.concatenate((strainRateLow, strainRateHigh))
    DIF = np.concatenate((DIFLow, DIFHigh))
    #
    DIFCurve = np.vstack((strainRate, DIF))
    #DIFCurve = np.vstack((strainRateLow, DIFLow))
    #
    return DIFCurve


def DIF_t(f_c):
    """
    Dynamic Increase Factor for tension.
    
    Parameters:
    -----------
    f_c : float
        Characteristic compressive strength of concrete (MPa)
        
    Returns:
    --------
    numpy.ndarray
        2D array with strain rates and corresponding DIF values
    """
    f_co = 10
    f_cs = f_c
    strainRateStatic = 3.0E-6
    strainRateMax = 300
    strainRateCutoff = 30
    #
    delta_s = 1.0/(10.0+6.0*f_cs/f_co)
    beta_s = pow(10, 7.11*delta_s-2.33)
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
    Calculate elastic stress using Hooke's law with elastic modulus from CEB data.
    
    Parameters:
    -----------
    f_c : float
        Characteristic compressive strength of concrete (MPa)
    strain : float or array-like
        Strain values
        
    Returns:
    --------
    float or array-like
        Elastic stress values (sigma_elastic = strain * E)
    """
    # Get CEB data including elastic modulus
    ceb = CEBClass(f_c=f_c)
    E = ceb.E
    
    return strain * E


# Backward compatibility: provide function that returns dictionary
def CEB(f_c=40, d_max=16.0, rho=2.4E-9, curve_array_size=100, delta_f=8.):
    """
    Backward compatibility function that returns CEB data as dictionary.
    
    Parameters:
    -----------
    f_c : float
        Characteristic compressive strength of concrete (MPa)
    d_max : float
        Maximum aggregate size (mm)
    rho : float
        Density (kg/mm^3)
    curve_array_size : int
        Number of points for stress-strain curves
    delta_f : float
        Difference between mean and characteristic strength (MPa)
        
    Returns:
    --------
    dict
        Dictionary containing all CEB material properties
    """
    ceb = CEBClass(f_c, d_max, rho, curve_array_size, delta_f)
    
    data = {}
    data['f_c'] = ceb.f_c
    data['f_cm0'] = ceb.f_cm0
    data['f_cm'] = ceb.f_cm
    data['f_t'] = ceb.f_t
    data['f_ctm'] = ceb.f_ctm
    data['f_tt'] = ceb.f_tt
    data['f_bc'] = ceb.f_bc
    data['G_fc'] = ceb.G_fc
    data['G_ft'] = ceb.G_ft
    data['G_fs'] = ceb.G_fs
    data['d_max'] = ceb.d_max
    data['rho'] = ceb.rho
    data['nu'] = ceb.nu
    data['E'] = ceb.E
    data['E_ci'] = ceb.E_ci
    data['E_c1'] = ceb.E_c1
    data['G'] = ceb.G
    data['K'] = ceb.K
    data['WF'] = ceb.WF
    data['epsilon_c1'] = ceb.epsilon_c1
    data['k'] = ceb.k
    data['compression_curve'] = ceb.compression_curve
    data['tension_curve'] = ceb.tension_curve
    data['crack_opening_curve'] = ceb.crack_opening_curve
    
    return data