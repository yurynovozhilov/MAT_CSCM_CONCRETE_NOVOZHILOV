import numpy as np
from enum import Enum
from CEB import CEBClass


class Revision(Enum):
    """Enumeration for CSCM model revisions."""
    REV_1 = 1
    REV_2 = 2
    REV_3 = 3


class MatCSCM:
    """
    Continuous Surface Cap Model (CSCM) for concrete material behavior.
    
    This class implements the CSCM material model for LS-DYNA, providing
    methods for calculating yield surfaces, damage parameters, strain rate
    effects, and generating material keywords.
    """
    
    def __init__(self, f_c=35, dmax=19, mid=159, rho=2.4E-9, nplot=1, 
                 incre=0, irate='on', erode='off', recov='full', 
                 itretrc=0, pred='off', repow=1, nh=0, ch=0, 
                 pwrc=5, pwrt=1, pmod=0):
        """
        Initialize CSCM material model.
        
        Parameters:
        -----------
        f_c : float
            Compressive strength (MPa)
        dmax : float
            Maximum aggregate size (mm)
        mid : int
            Material ID
        rho : float
            Density
        nplot : int
            Plot option (1-7)
        incre : float
            Maximum strain increment for subincrementation
        irate : str
            Rate effects model ('on'/'off')
        erode : str
            Erosion option ('off' or float value)
        recov : str
            Modulus recovery option ('full' or float value)
        itretrc : int
            Cap retraction option (0/1)
        pred : str
            Preexisting damage ('off' or float value)
        repow : float
            Power that increases fracture energy with rate effects
        nh : float
            Hardening initiation
        ch : float
            Hardening rate
        pwrc : float
            Shear-to-compression transition parameter
        pwrt : float
            Shear-to-tension transition parameter
        pmod : float
            Modify moderate pressure softening parameter
        """
        self.f_c = f_c
        self.dmax = dmax
        self.mid = mid
        self.rho = rho
        self.nplot = nplot
        self.incre = incre
        self.irate = 1 if irate == 'on' else 0
        self.erode = 0.99 if erode == 'off' else 1 + float(erode)
        self.recov = 0 if recov == 'full' else 1 - float(recov)
        self.itretrc = itretrc
        self.pred = 0 if pred == 'off' else float(pred)
        self.repow = repow
        self.nh = nh
        self.ch = ch
        self.pwrc = pwrc
        self.pwrt = pwrt
        self.pmod = pmod
        
        # Element size for damage calculations
        self.esize = 200
        
        # Get CEB material properties
        self.ceb_data = CEBClass(f_c=f_c, d_max=dmax)
        
        # Initialize nested classes
        self.yield_surface = self.YieldSurface(self)
        self.damage = self.Damage(self)
        self.strain_rate = self.StrainRate(self)
        self.cap_surface = self.CapSurface(self)
    
    
    class YieldSurface:
        """Yield surface calculations for CSCM model."""
        
        def __init__(self, parent):
            self.parent = parent
        
        def P(self, A_p, B_p, C_p):
            """Polynomial function for parameter calculations."""
            f_c = self.parent.f_c
            return A_p * pow(f_c, 2) + B_p * f_c + C_p
        
        def F_f(self, I, rev=Revision.REV_3):
            """
            Shear surface F_f defined along the compression meridian TXC.
            
            Parameters:
            -----------
            I : array_like
                First stress invariant
            rev : Revision
                Revision number (REV_1, REV_2, or REV_3)
            """
            f_c = self.parent.f_c
            result = self.alpha(rev)
            result -= self.lamda(rev) * np.exp(-self.beta(rev) * I)
            result += self.theta(rev) * I
            return result
        
        # Compression meridian (TXC) parameters
        def alpha(self, rev=Revision.REV_3):
            """Alpha parameter for compression meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(-0.003, 0.3169747, 7.7047)
                case Revision.REV_2:
                    return 13.9846 * np.exp(f_c / 68.8756) - 13.8981
                case Revision.REV_3:
                    return 2.5801E-03 * pow(f_c, 2) + 1.6405E-01 * f_c + 4.3506E-01
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def lamda(self, rev=Revision.REV_3):
            """Lambda parameter for compression meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(0.0, 0.0, 10.5)
                case Revision.REV_2:
                    return 3.6657 * np.exp(f_c / 39.9363) - 4.7092
                case Revision.REV_3:
                    return 3.0220E-03 * pow(f_c, 2.0231E+00)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def beta(self, rev=Revision.REV_3):
            """Beta parameter for compression meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(0.0, 0.0, 1.929E-02)
                case Revision.REV_2:
                    return 18.17791 * pow(f_c, -1.7163)
                case Revision.REV_3:
                    return 1.2317E+01 * pow(f_c, -1.5974E+00)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def theta(self, rev=Revision.REV_3):
            """Theta parameter for compression meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(1.3216E-05, 2.3548E-03, 0.2140058)
                case Revision.REV_2:
                    return 0.3533 - 3.3294E-4 * f_c - 3.8182E-6 * pow(f_c, 2)
                case Revision.REV_3:
                    return -3.4286E-06 * pow(f_c, 2) - 3.7971E-04 * f_c + 3.5436E-01
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def TXC(self, I, rev=Revision.REV_3):
            """Compression meridian."""
            return self.F_f(I, rev)
        
        # Shear meridian (TOR) parameters
        def alpha_1(self, rev=Revision.REV_3):
            """Alpha_1 parameter for shear meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(0, 0, 0.74735)
                case Revision.REV_2:
                    return 0.82
                case Revision.REV_3:
                    return 1 / np.sqrt(3.0) + self.lamda_1(rev)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def lamda_1(self, rev=Revision.REV_3):
            """Lambda_1 parameter for shear meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(0, 0, 0.17)
                case Revision.REV_2:
                    return 0.2407
                case Revision.REV_3:
                    return (-2.0833E-07 * pow(f_c, 3) + 3.7571E-05 * pow(f_c, 2) - 
                            2.3049E-03 * f_c + 2.8860E-01)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def beta_1(self, rev=Revision.REV_3):
            """Beta_1 parameter for shear meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(-1.9972e-05, 2.2655e-04, 8.1748e-02)
                case Revision.REV_2:
                    return 0.33565 * pow(f_c, -0.95383)
                case Revision.REV_3:
                    return 3.4093E-01 * pow(f_c, -9.4944E-01)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def theta_1(self, rev=Revision.REV_3):
            """Theta_1 parameter for shear meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(-4.0856E-07, -1.2132E-06, 1.5593E-03)
                case Revision.REV_2:
                    return 0
                case Revision.REV_3:
                    return 0
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def Q_1(self, I, rev=Revision.REV_3):
            """Q_1 strength ratio for shear meridian."""
            f_c = self.parent.f_c
            if not isinstance(I, np.ndarray):
                I = np.array([I])
            
            for i, value in enumerate(I):
                if value >= 0:
                    # TOR/TXC strength ratio
                    return (self.alpha_1(rev) - self.lamda_1(rev) * 
                            np.exp(-self.beta_1(rev) * i) + self.theta_1(rev) * i)
                else:
                    # Values to simulate triangular yield surface in deviatoric plane for tensile pressure
                    return 1 / np.sqrt(3.0)
        
        def TOR(self, I, rev=Revision.REV_3):
            """Shear meridian."""
            I_tension = I[I <= 0]
            I_compression = I[I > 0]
            result_negative = 1.0 / np.sqrt(3.0) * self.TXC(I_tension, rev)
            result_compression = self.Q_1(I_compression, rev) * self.TXC(I_compression, rev)
            return np.hstack((result_negative, result_compression))
        
        # Tensile meridian (TXE) parameters
        def alpha_2(self, rev=Revision.REV_3):
            """Alpha_2 parameter for tensile meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(0, 0, 0.66)
                case Revision.REV_2:
                    return 0.76
                case Revision.REV_3:
                    return round(0.5 + self.lamda_2(rev), 4)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def lamda_2(self, rev=Revision.REV_3):
            """Lambda_2 parameter for tensile meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(0, 0, 0.16)
                case Revision.REV_2:
                    return 0.26
                case Revision.REV_3:
                    return 3.0029E-01 * pow(f_c, -4.2269E-02)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def beta_2(self, rev=Revision.REV_3):
            """Beta_2 parameter for tensile meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(-1.9972e-05, 2.2655e-04, 8.2748e-02)
                case Revision.REV_2:
                    return 0.285 * pow(f_c, -0.94843)
                case Revision.REV_3:
                    return 2.8898E-01 * pow(f_c, -9.4776E-01)
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def theta_2(self, rev=Revision.REV_3):
            """Theta_2 parameter for tensile meridian."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.P(-4.8697e-07, -1.8883e-06, 1.8822e-03)
                case Revision.REV_2:
                    return 0
                case Revision.REV_3:
                    return 0
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def Q_2(self, I, rev=Revision.REV_3):
            """Q_2 strength ratio for tensile meridian."""
            f_c = self.parent.f_c
            if not isinstance(I, np.ndarray):
                I = np.array([I])
            
            for i, value in enumerate(I):
                if i >= 0:
                    # TXE/TXC strength ratio
                    return (self.alpha_2(rev) - self.lamda_2(rev) * 
                            np.exp(-self.beta_2(rev) * i) + self.theta_2(rev) * i)
                else:
                    # Values to simulate triangular yield surface in deviatoric plane for tensile pressure
                    return 0.5
        
        def TXE(self, I, rev=Revision.REV_3):
            """Tensile meridian."""
            I_tension = I[I <= 0]
            I_compression = I[I > 0]
            result_negative = 0.5 * self.TXC(I_tension, rev)
            result_compression = self.Q_2(I_compression, rev) * self.TXC(I_compression, rev)
            return np.hstack((result_negative, result_compression))
        
        def Rubin(self, I, rev=Revision.REV_3, resolution=30):
            """Rubin yield surface calculation."""
            beta_hat = np.linspace(-np.pi / 6.0, np.pi, resolution)
            
            q1 = self.Q_1(I, rev)
            q2 = self.Q_2(I, rev)
            
            a_0 = 2 * pow(q1, 2) * (q2 - 1)
            a_1 = np.sqrt(3) * q2 + 2 * q1 * (q2 - 1)
            a_2 = q2
            a = (-a_1 + np.sqrt(pow(a_1, 2) - 4 * a_2 * a_0)) / (2 * a_2)
            
            b = pow(2 * q1 + a, 2) - 3
            b_0 = -(3 + b - pow(a, 2)) / 4
            b_1 = a * (np.cos(beta_hat) - a * np.sin(beta_hat))
            b_2 = pow(np.cos(beta_hat) - a * np.sin(beta_hat), 2) + b * pow(np.sin(beta_hat), 2)
            
            RScale = (-b_1 + np.sqrt(pow(b_1, 2) - 4 * b_2 * b_0)) / (2 * b_2)
            
            RCurve = np.vstack((beta_hat, RScale))
            return RCurve
        
        def f(self, I_1, J_2, kappa, kappa_0, rev=Revision.REV_3):
            """
            General yield function f = F_f(I_1) * F_c(I_1, J_2, kappa) - kappa.
            
            This function combines the shear failure surface F_f and the cap 
            failure surface F_c to define the overall yield criterion for the 
            CSCM model.
            
            Parameters:
            -----------
            I_1 : array_like
                First stress invariant (I1)
            J_2 : array_like
                Second stress invariant (J2)
            kappa : array_like
                Hardening parameter that controls cap expansion/contraction
            kappa_0 : float
                Initial value of kappa at the intersection of cap and shear surfaces
            rev : Revision
                Revision number (REV_1, REV_2, or REV_3)
                
            Returns:
            --------
            array_like
                Yield function value. f < 0: elastic, f = 0: yield, f > 0: inadmissible
            """
            # Calculate shear failure surface F_f(I_1)
            F_f_value = self.F_f(I_1, rev)
            
            # Calculate cap failure surface F_c(I_1, kappa, kappa_0)
            # Access cap surface through parent object
            F_c_value = self.parent.cap_surface.F_c(I_1, kappa, kappa_0, rev)
            
            # General yield function: f = F_f * F_c - kappa
            yield_function = F_f_value * F_c_value - kappa
            
            return yield_function
    
    
    class CapSurface:
        """Cap surface calculations for CSCM model."""
        
        def __init__(self, parent):
            self.parent = parent
        
        def X0(self, rev=Revision.REV_3):
            """Initial location of the cap when kappa = kappa_0."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return self.parent.yield_surface.P(8.769178e-03, -7.3302306e-02, 84.85)
                case Revision.REV_2:
                    return 17.087 + 1.892 * f_c
                case Revision.REV_3:
                    return 4.0224E+00 * f_c - 7.0784E+01
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def R(self, rev=Revision.REV_3):
            """Ellipticity ratio - ratio of major to minor ellipse axes."""
            f_c = self.parent.f_c
            match rev:
                case Revision.REV_1:
                    return 5
                case Revision.REV_2:
                    return 4.45994 * np.exp(-f_c / 11.51679) + 1.95358
                case Revision.REV_3:
                    return 5.0000E-04 * pow(f_c, 2) - 5.9000E-02 * f_c + 3.6600E+00
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def W(self, rev=Revision.REV_3):
            """
            Maximum plastic volume strain.
            
            The maximum plastic volume change sets the range in volumetric strain over 
            which the pressure-volumetric strain curve is nonlinear (from onset to lock-up). 
            Typically, the maximum plastic volume change is approximately equal 
            to the porosity of the air voids. A value of 0.05 indicates an air void 
            porosity of 5 percent.
            """
            match rev:
                case Revision.REV_1:
                    return 0.05
                case Revision.REV_2:
                    return 0.065
                case Revision.REV_3:
                    return 0.065
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def D_1(self, rev=Revision.REV_3):
            """D_1 parameter for cap surface."""
            match rev:
                case Revision.REV_1:
                    return 2.5E-4
                case Revision.REV_2:
                    return 6.11e-4
                case Revision.REV_3:
                    return 6.11e-4
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def D_2(self, rev=Revision.REV_3):
            """D_2 parameter for cap surface."""
            match rev:
                case Revision.REV_1:
                    return 3.49E-7
                case Revision.REV_2:
                    return 2.225E-6
                case Revision.REV_3:
                    return 2.225E-6
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def L(self, kappa, kappa_0):
            """
            L(kappa) is the position on the I-axis where 
            the ellipse (cap surface) intersects 
            the shear failure surface.
            
            kappa_0 is the value of I at the initial intersection 
            of the cap and shear surfaces before hardening 
            is engaged (before the cap moves).
            """
            # Handle both scalar and array inputs
            kappa = np.asarray(kappa)
            return np.maximum(kappa, kappa_0)
        
        def X(self, I, kappa, kappa_0, rev=Revision.REV_3):
            """
            X(kappa) is the position on the I-axis where the outer
            edge of the ellipse (cap surface) intersects.
            """
            return (self.L(kappa, kappa_0) + 
                    self.R(rev) * self.parent.yield_surface.F_f(self.L(kappa, kappa_0), rev))
        
        def F_c(self, I, kappa, kappa_0, rev=Revision.REV_3):
            """
            Cap failure surface function F_c.
            kappa is a hardening parameter that causes the cap 
            surface to move (expand or contract).
            """
            # Ensure inputs are arrays
            I = np.asarray(I)
            kappa = np.asarray(kappa)
            
            result = (I - self.L(kappa, kappa_0))
            result *= (np.abs(result) + result)
            result /= (2 * pow(self.X0(rev), 2))
            result = 1 - result
            
            # Clip negative values to zero
            result = np.maximum(result, 0)
            return result
        
        def epsilon_v_p(self, X, rev=Revision.REV_3):
            """
            Plastic volume strain - basis for motion (expansion and contraction) of the cap.
            """
            return (self.W(rev) * 
                    (1 - np.exp(-self.D_1(rev) * (X - self.X0(rev)) - 
                                self.D_2(rev) * pow(X - self.X0(rev), 2))))
        
        def hydrostatic_compression_parameters(self, X, rev=Revision.REV_3):
            """Hydrostatic compression parameters."""
            return (self.D_1(rev) * (X - self.X0(rev)) + 
                    self.D_2(rev) * pow(X - self.X0(rev), 2))
        
        def kappa(self, delta_epsilon_p, epsilon_v_p_old, kappa_0, rev=Revision.REV_3):
            """
            Calculate new kappa value based on plastic strain increment.
            
            This function implements the cap hardening algorithm that updates the 
            position of the cap surface based on plastic volumetric strain evolution.
            
            Parameters:
            -----------
            delta_epsilon_p : float
                Plastic strain increment
            epsilon_v_p_old : float
                Previous plastic volumetric strain
            kappa_0 : float
                Initial kappa value (cap cannot shrink below this value)
            rev : Revision
                Revision number (REV_1, REV_2, or REV_3)
                
            Returns:
            --------
            tuple
                (kappa_new, epsilon_v_p_new) - Updated kappa and plastic volumetric strain
            """
            # Get material parameters
            nu = self.parent.ceb_data.nu  # Poisson's ratio
            W = self.W(rev)                  # Maximum plastic volume strain
            D1 = self.D_1(rev)              # D1 parameter
            D2 = self.D_2(rev)              # D2 parameter
            X0 = self.X0(rev)               # Initial cap position
            R = self.R(rev)                 # Ellipticity ratio
            
            # Step 1: Calculate plastic volumetric strain increment
            # Account for dilatancy during compression
            delta_epsilon_v_p = delta_epsilon_p * (1 - 2 * nu)
            
            # Step 2: Update total plastic volumetric strain
            epsilon_v_p_new = epsilon_v_p_old + delta_epsilon_v_p
            
            # Step 3: Normalize plastic volumetric strain
            epsilon_v_p_norm = abs(epsilon_v_p_new) / W
            
            # Step 4: Calculate new cap position
            exp_term = np.exp(-D1 * epsilon_v_p_norm - D2 * epsilon_v_p_norm**2)
            X_new = X0 + epsilon_v_p_norm * (1 - exp_term)
            
            # Step 5: Calculate new kappa through inverse relationship
            kappa_new = (X_new + R**2 * kappa_0) / (1 + R**2)
            
            # Cap cannot shrink below initial position
            kappa_new = max(kappa_new, kappa_0)
            
            return kappa_new, epsilon_v_p_new
    
    
    class Damage:
        """Damage calculations for CSCM model."""
        
        def __init__(self, parent):
            self.parent = parent
        
        def B(self, rev=Revision.REV_1):
            """Ductile shape softening parameter."""
            f_c = self.parent.f_c
            E = self.parent.ceb_data.E
            G_f_c = self.parent.ceb_data.G_fc
            l = self.parent.esize
            
            match rev:
                case Revision.REV_1:
                    return 100
                case Revision.REV_2:
                    bfit = 2.0 * G_f_c / l
                    bfit += f_c * 2 / E
                    bfit = pow(bfit, 0.5)
                    bfit += f_c / pow(E, 0.5)
                    bfit /= G_f_c / l
                    return bfit
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def D(self, rev=Revision.REV_1):
            """Brittle shape softening parameter."""
            f_t = self.parent.ceb_data.f_t
            E = self.parent.ceb_data.E
            G_ft = self.parent.ceb_data.G_ft
            l = self.parent.esize
            
            match rev:
                case Revision.REV_1:
                    return 0.1
                case Revision.REV_2:
                    return l * f_t / (G_ft * pow(E, 0.5))
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def pmod(self):
            """
            Modify moderate pressure softening parameter.
            
            In addition to reducing the maximum damage level with confinement (pressure), 
            the compressive softening parameter, A, may also be reduced with confinement.
            
            A *= pow((d_max+0.001),pmod)
            
            Here pmod is a user-specified input parameter. Its default value is 0.0. 
            Input compression value of pmod reduces A when the maximum damage is less than 0.999; 
            otherwise A is unaffected by pmod. Thus, it is only active at moderate confinement levels.
            """
            return 0.0
        
        def brittle_damage(self, tau_b, D, C, d_max, r_0b):
            """Calculate brittle damage."""
            d = (1 + D)
            d /= (1 + D * np.exp(-C * (tau_b - r_0b)))
            d -= 1
            d *= d_max / D
            return d
        
        def ductile_damage(self, tau_d, B, a, d_max, r_0d):
            """Calculate ductile damage."""
            d = (1 + B)
            d /= (1 + B * np.exp(-a * (tau_d - r_0d)))
            d -= 1
            d *= d_max / B
            return d
    
    
    class StrainRate:
        """Strain rate effects for CSCM model."""
        
        def __init__(self, parent):
            self.parent = parent
        
        def n_t(self, rev=Revision.REV_1):
            """n_t parameter for tensile strain rate."""
            match rev:
                case Revision.REV_1:
                    return 0.48
                case Revision.REV_2:
                    return 0
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def eta_0_t(self, rev=Revision.REV_1):
            """eta_0_t parameter for tensile strain rate."""
            f_c = self.parent.f_c
            f_c_in_psi = f_c * 145.0377
            match rev:
                case Revision.REV_1:
                    return self.parent.yield_surface.P(8.0614774E-13, -9.77736719E-10, 5.0752351E-05)
                case Revision.REV_2:
                    return 0
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def eta_t(self, strain_rate, rev=Revision.REV_1):
            """Fluidity parameter in uniaxial tensile stress."""
            return self.eta_0_t(rev) / pow(strain_rate, self.n_t(rev))
        
        def n_c(self, rev=Revision.REV_1):
            """n_c parameter for compressive strain rate."""
            match rev:
                case Revision.REV_1:
                    return 0.78
                case Revision.REV_2:
                    return 0
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def eta_0_c(self, rev=Revision.REV_1):
            """eta_0_c parameter for compressive strain rate."""
            f_c = self.parent.f_c
            f_c_in_psi = f_c * 145.0377
            match rev:
                case Revision.REV_1:
                    return self.parent.yield_surface.P(1.2772337E-11, -1.0613722E-07, 3.203497E-4)
                case Revision.REV_2:
                    return 0
                case _:
                    raise ValueError(f"Invalid revision number: {rev}")
        
        def eta_c(self, strain_rate, rev=Revision.REV_1):
            """Fluidity parameter in uniaxial compressive stress."""
            return self.eta_0_c(rev) / pow(strain_rate, self.n_c(rev))
        
        def eta_s(self, strain_rate, rev=Revision.REV_1):
            """Fluidity parameter in shear stress."""
            return self.Srate(rev) * self.eta_t(strain_rate, rev)
        
        def Srate(self, rev=Revision.REV_1):
            """Ratio of effective shear stress to tensile stress fluidity parameters."""
            return 1.0
        
        def overt(self, rev=Revision.REV_1):
            """Over-stress limit for tension."""
            f_c = self.parent.f_c
            return self.parent.yield_surface.P(1.309663E-02, -0.3927659, 21.45)
        
        def overc(self, rev=Revision.REV_1):
            """Over-stress limit for compression."""
            return self.overt(rev)
        
        def DIF_CSCM_t(self, rev=Revision.REV_1, strain_rate_max=1000):
            """Dynamic Increase Factor for tension."""
            f_t = self.parent.ceb_data.f_t
            E = self.parent.ceb_data.E
            over_tension = self.overt(rev)
            
            strain_rate_static = 30.0E-6
            strain_rate = np.linspace(strain_rate_static, strain_rate_max, strain_rate_max)
            
            inviscid_strengths = f_t
            viscoplastic_strengths = E * strain_rate * self.eta_t(strain_rate, rev)
            
            for i, strengths in enumerate(viscoplastic_strengths):
                if strengths > over_tension:
                    viscoplastic_strengths[i] = over_tension
            
            DIF = viscoplastic_strengths / inviscid_strengths + 1
            DIF_curve = np.vstack((strain_rate, DIF))
            return DIF_curve
        
        def DIF_CSCM_c(self, rev=Revision.REV_1, strain_rate_max=1000):
            """Dynamic Increase Factor for compression."""
            f_c = self.parent.f_c
            E = self.parent.ceb_data.E
            over_compression = self.overc(rev)
            
            strain_rate_static = 30.0E-6
            strain_rate = np.linspace(strain_rate_static, strain_rate_max, strain_rate_max)
            
            inviscid_strengths = f_c
            viscoplastic_strengths = E * strain_rate * self.eta_c(strain_rate, rev)
            
            for i, strengths in enumerate(viscoplastic_strengths):
                if strengths > over_compression:
                    viscoplastic_strengths[i] = over_compression
            
            DIF = viscoplastic_strengths / inviscid_strengths + 1
            DIF_curve = np.vstack((strain_rate, DIF))
            return DIF_curve
    
    
    def generate_keyword(self):
        """
        Generate LS-DYNA material keyword for CSCM.
        
        Returns:
        --------
        dict
            Dictionary containing all material parameters for LS-DYNA keyword generation
        """
        # Convert CEB class to dictionary for compatibility
        from CEB import CEB
        data = CEB(f_c=self.f_c, d_max=self.dmax, rho=self.rho)
        
        CSCM = {}
        CSCM['NAME'] = '*MAT_CSCM'
        
        # Card 1
        CSCM['MID'] = {'card': 1, 'position': 1, 'type': 'A8', 'value': self.mid}
        CSCM['RHO'] = {'card': 1, 'position': 2, 'type': 'F', 'value': self.rho}
        CSCM['NPLOT'] = {'card': 1, 'position': 3, 'type': 'I', 'value': self.nplot}
        CSCM['INCRE'] = {'card': 1, 'position': 4, 'type': 'F', 'value': self.incre}
        CSCM['IRATE'] = {'card': 1, 'position': 5, 'type': 'I', 'value': self.irate}
        CSCM['ERODE'] = {'card': 1, 'position': 6, 'type': 'F', 'value': self.erode}
        CSCM['RECOV'] = {'card': 1, 'position': 7, 'type': 'F', 'value': self.recov}
        CSCM['ITRETRC'] = {'card': 1, 'position': 8, 'type': 'I', 'value': self.itretrc}
        
        # Card 2
        CSCM['PRED'] = {'card': 2, 'position': 1, 'type': 'F', 'value': self.pred}
        
        # Card 3
        CSCM['G'] = {'card': 3, 'position': 1, 'type': 'F', 'value': data['G']}
        CSCM['K'] = {'card': 3, 'position': 2, 'type': 'F', 'value': data['K']}
        CSCM['ALPHA'] = {'card': 3, 'position': 3, 'type': 'F', 'value': self.yield_surface.alpha(Revision.REV_2)}
        CSCM['THETA'] = {'card': 3, 'position': 4, 'type': 'F', 'value': self.yield_surface.theta(Revision.REV_2)}
        CSCM['LAMBDA'] = {'card': 3, 'position': 5, 'type': 'F', 'value': self.yield_surface.lamda(Revision.REV_2)}
        CSCM['BETA'] = {'card': 3, 'position': 6, 'type': 'F', 'value': self.yield_surface.beta(Revision.REV_2)}
        CSCM['NH'] = {'card': 3, 'position': 7, 'type': 'F', 'value': self.nh}
        CSCM['CH'] = {'card': 3, 'position': 8, 'type': 'F', 'value': self.ch}
        
        # Card 4
        CSCM['ALPHA1'] = {'card': 4, 'position': 1, 'type': 'F', 'value': self.yield_surface.alpha_1(Revision.REV_2)}
        CSCM['THETA1'] = {'card': 4, 'position': 2, 'type': 'F', 'value': self.yield_surface.theta_1(Revision.REV_2)}
        CSCM['LAMBDA1'] = {'card': 4, 'position': 3, 'type': 'F', 'value': self.yield_surface.lamda_1(Revision.REV_2)}
        CSCM['BETA1'] = {'card': 4, 'position': 4, 'type': 'F', 'value': self.yield_surface.beta_1(Revision.REV_2)}
        CSCM['ALPHA2'] = {'card': 4, 'position': 5, 'type': 'F', 'value': self.yield_surface.alpha_2(Revision.REV_2)}
        CSCM['THETA2'] = {'card': 4, 'position': 6, 'type': 'F', 'value': self.yield_surface.theta_2(Revision.REV_2)}
        CSCM['LAMBDA2'] = {'card': 4, 'position': 7, 'type': 'F', 'value': self.yield_surface.lamda_2(Revision.REV_2)}
        CSCM['BETA2'] = {'card': 4, 'position': 8, 'type': 'F', 'value': self.yield_surface.beta_2(Revision.REV_2)}
        
        # Card 5
        CSCM['R'] = {'card': 5, 'position': 1, 'type': 'F', 'value': self.cap_surface.R(Revision.REV_2)}
        CSCM['X0'] = {'card': 5, 'position': 2, 'type': 'F', 'value': self.cap_surface.X0(Revision.REV_2)}
        CSCM['W'] = {'card': 5, 'position': 3, 'type': 'F', 'value': self.cap_surface.W(Revision.REV_2)}
        CSCM['D1'] = {'card': 5, 'position': 4, 'type': 'F', 'value': self.cap_surface.D_1(Revision.REV_2)}
        CSCM['D2'] = {'card': 5, 'position': 5, 'type': 'F', 'value': self.cap_surface.D_2(Revision.REV_2)}
        
        # Card 6
        CSCM['B'] = {'card': 6, 'position': 1, 'type': 'F', 'value': self.damage.B(Revision.REV_1)}
        CSCM['GFC'] = {'card': 6, 'position': 2, 'type': 'F', 'value': data['G_fc']}
        CSCM['D'] = {'card': 6, 'position': 3, 'type': 'F', 'value': self.damage.D(Revision.REV_1)}
        CSCM['GFT'] = {'card': 6, 'position': 4, 'type': 'F', 'value': data['G_ft']}
        CSCM['GFS'] = {'card': 6, 'position': 5, 'type': 'F', 'value': data['G_fs']}
        CSCM['PWRC'] = {'card': 6, 'position': 6, 'type': 'F', 'value': self.pwrc}
        CSCM['PWRT'] = {'card': 6, 'position': 7, 'type': 'F', 'value': self.pwrt}
        CSCM['PMOD'] = {'card': 6, 'position': 8, 'type': 'F', 'value': self.pmod}
        
        # Card 7
        CSCM['ETA_0_C'] = {'card': 7, 'position': 1, 'type': 'F', 'value': self.strain_rate.eta_0_c(Revision.REV_1)}
        CSCM['N_C'] = {'card': 7, 'position': 2, 'type': 'F', 'value': self.strain_rate.n_c(Revision.REV_1)}
        CSCM['ETA_0_T'] = {'card': 7, 'position': 3, 'type': 'F', 'value': self.strain_rate.eta_0_t(Revision.REV_1)}
        CSCM['N_T'] = {'card': 7, 'position': 4, 'type': 'F', 'value': self.strain_rate.n_t(Revision.REV_1)}
        CSCM['OVERC'] = {'card': 7, 'position': 5, 'type': 'F', 'value': self.strain_rate.overc(Revision.REV_1)}
        CSCM['OVERT'] = {'card': 7, 'position': 6, 'type': 'F', 'value': self.strain_rate.overt(Revision.REV_1)}
        CSCM['SRATE'] = {'card': 7, 'position': 7, 'type': 'F', 'value': self.strain_rate.Srate(Revision.REV_1)}
        CSCM['REPOW'] = {'card': 7, 'position': 8, 'type': 'F', 'value': self.repow}
        
        return CSCM
    
    def get_ceb_output(self):
        """
        Generate CEB-FIP estimation output text.
        
        Returns:
        --------
        str
            Formatted text with CEB-FIP estimations
        """
        # Convert CEB class to dictionary for compatibility
        from CEB import CEB
        items = CEB(f_c=self.f_c, d_max=self.dmax, rho=self.rho)
        text = '$#\n'
        text += '$# CEBFIP Estimations:\n'
        for key in items:
            if not isinstance(items[key], np.ndarray):
                text += '$# {0} = {1:G}\n'.format(key, items[key])
        text += '$#\n'
        return text


def keyword_to_text(data, word_length=10, word_number=8):
    """
    Convert material keyword dictionary to formatted text.
    
    Parameters:
    -----------
    data : dict
        Material keyword dictionary
    word_length : int
        Word length for formatting
    word_number : int
        Number of words per line
    
    Returns:
    --------
    str
        Formatted keyword text
    """
    empty_card = ' ' * word_length * word_number
    card_count = 0
    plane_text = ''
    items = list(data.keys())[1:]
    keyword_text = [data['NAME']]
    
    for key in items:
        if int(data[key]['card']) > card_count:
            card_count = data[key]['card']
            keyword_text.append('')
            keyword_text.append('')
        
        if data[key]['position'] == 1:
            keyword_text[2 * card_count - 1] += '$#{0: >{1}s}'.format(key, word_length - 2)
        else:
            keyword_text[2 * card_count - 1] += ' {0: >{1}s}'.format(key, word_length - 1)
        
        if data[key]['value'] == 'AUTO':
            keyword_text[2 * card_count] += '{0}'.format(' ' * word_length)
        else:
            if data[key]['type'] == 'A8':
                keyword_text[2 * card_count] += ' {0:>{1}s}'.format(str(data[key]['value']), word_length - 1)
            elif data[key]['type'] == 'I':
                keyword_text[2 * card_count] += ' {0:>{1}d}'.format(int(data[key]['value']), word_length - 1)
            elif data[key]['type'] == 'F':
                keyword_text[2 * card_count] += ' {0:{1}.{2}G}'.format(float(data[key]['value']), word_length - 1, word_length - 6)
            else:
                keyword_text[2 * card_count] += '{0}'.format(' ' * word_length)
    
    for lines in keyword_text:
        plane_text += lines + '\n'
    
    return plane_text