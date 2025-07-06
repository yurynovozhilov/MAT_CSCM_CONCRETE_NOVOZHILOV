# coding: utf-8

import os
import matplotlib.pyplot as plt
import numpy as np
import pyperclip
from collections import OrderedDict as OD
from pint import UnitRegistry

def CEBFIB(fc, dmax, rho = 2.4E-9):
    ################################################
    # Compressive strength
    # (CEB-FIB Model Code 2010 5.1.4)
    # specific characteristic compressive strength 
    fck     = fc
    # MPa
    delta_f = 8.
    # mean compressive strength
    fcm     = fck + delta_f 
    # biaxial compression strength, MPa
    fbc     = 1.15*fck
    ################################################
    # Tensile strength
    # (CEB-FIB Model Code 2010 5.1.5.1)
    # mean value of tensile strenght for fck <= C50
    if fck <= 50:
        fctm = 0.3*pow(fck,2./3.)
    # mean value of tensile strenght for fck >  C50
    else:
        fctm = 2.12*np.log(1+0.1*(fck+delta_f))
    # lower bounds for characteristic tensile strenght
    fck_min = 0.7*fctm
    # upper bounds for characteristic tensile strenght
    fck_max = 1.3*fctm
    # uniaxial tensile strenght
    ft      = fctm
    # biaxial tensile strength
    fbt     = ft
    # triaxial tensile strength
    ftt     = ft
    ################################################
    # Fracture energy
    # (CEB-FIB Model Code 2010 5.1.5.2)             
    # Gf = 73*pow(fcm,0.18) # fracture energy
    # MPa
    fcm0    = 10.0                                  
    # Base value for fracture energy, Nmm/mm^2
    Gf0     = 0.021+5.357E-4*dmax
    # Fracture energy, Nmm/mm^2
    Gft      = Gf0*pow(fcm/fcm0, 0.7)
    Gfc      = Gft*100
    Gfs      = Gft
    ################################################
    # Elastic poperties 
    # (CEB-FIB Model Code 2010 5.1.7.2)
    # MPa
    Ec0     = 2.15E+4
    # aggregate qualititive values
    alpha_E = 1.0
    # Elacticity modulud at 28 day
    Eci = Ec0*alpha_E*pow((fck+delta_f)/fcm0,1./3.) 
    alpha_i = 0.8+0.2*fcm/88
    if alpha_i > 1.0: 
        alpha_i = 1.0
    # Reduced elasticity modulus 
    Ec  = alpha_i*Eci                               
    E   = Eci
    # Poisson ratio for stresses -0.6*fck < sigma <0.8*fctk
    nu  = 0.2                                       
    # Shear modulus
    G   = E/(2.*(1+nu))                             
    # Bulk modulus
    K   = E/(3.*(1-2.*nu))                          
    ################################################
    # MAT_CONCRETE_DAMAGE_PLASTIC_MODEL stecial data
    # Tensile softening branch for exponential tensile damage formulation
    # WF  = Gf/ft
    # ksi = ft*(fbc**2-fc**2)/(fbc*(fc**2-ft**2))
    # ECC = (1+ksi)/(1-ksi)
    ################################################
    # Record data from CEB-FIB estimations
    data = OD()
    data['fc']   = fc  
    data['fcm']  = fcm 
    data['fcm']  = fcm   
    data['ft']   = ft 
    data['ftt']  = ftt     
    data['fbc']  = fbc 
    data['Gfc']  = Gfc
    data['Gft']  = Gft     
    data['Gfs']  = Gfs     
    data['dmax'] = dmax
    data['rho']  = rho 
    data['nu']   = nu     
    data['E']    = E       
    data['G']    = G       
    data['K']    = K 
    #data['WF']   = WF
    #data['ECC']  = ECC    
    return data

def P(fc, Ap,Bp,Cp):
    return Ap*pow(fc,2)+Bp*fc+Cp

def concPlot(x,
             y1,
             y2,
             lable1='rev 1', 
             label2='rev 2', 
             xLabel='Ox',
             yLabel='Oy',
             fontsize=15, 
             imgSizeYinches=10, 
             imgSizeXinches=15,
             linewidth=2.0,
             xlim_0 = -100,
             xlim_1 = 100,
             ylim_0 = -100,
             ylim_1 = 100,
            ):

    fig = plt.figure()
    ax = fig.add_subplot(111)

    fig.set_size_inches(imgSizeXinches, imgSizeYinches, forward=True)

    ax.plot(x, y1, label = u'rev = 1',color='blue',linewidth=2.0)
    ax.plot(x, y2, label = u'rev = 2',color='red',linewidth=2.0)

    ax.grid(True)
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    
    ax.set_xlim([xlim_0,xlim_1])
    ax.set_ylim([ylim_0,ylim_1])
    
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))

    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))

    for label in ax.xaxis.get_ticklabels(): label.set_fontsize(fontsize)
    for label in ax.yaxis.get_ticklabels(): label.set_fontsize(fontsize)

    plt.legend(loc='upper left',prop={'size':fontsize+4})
    plt.xlabel(xLabel).set_fontsize(fontsize+4)
    plt.ylabel(yLabel).set_fontsize(fontsize+4)
    plt.show()
    return 

def alpha(fc,rev=1):
    if rev   == 1: return P(fc, -0.003, 0.3169747, 7.7047)
    elif rev == 2: return 13.9846*np.exp(fc/68.8756)-13.8981
    else: return False 

def lamda(fc,rev=1):
    if   rev == 1: return P(fc, 0.0, 0.0, 10.5)
    elif rev == 2: return 3.6657*np.exp(fc/39.9363)-4.7092
    else: return False 

def beta(fc,rev=1):
    if rev   == 1: return P(fc, 0.0, 0.0, 1.929E-02)
    elif rev == 2: return 18.17791*pow(fc,-1.7163)
    else: return False 

def theta(fc,rev=1):
    if   rev == 1: return P(fc, 1.3216E-05, 2.3548E-03, 0.2140058)
    elif rev == 2: return 0.3533-3.3294E-4*fc-3.8182E-6*pow(fc,2)
    else: return False 

def TXC(fc, J, rev):
    return alpha(fc,rev)-lamda(fc,rev)*np.exp(-beta(fc,rev)*J)+theta(fc,rev)*J

def alpha1(fc,rev=1):
    if rev   == 1: return P(fc, 0, 0, 0.74735)
    elif rev == 2: return 0.82
    else: return False 

def lamda1(fc,rev=1):
    if   rev == 1: return P(fc, 0, 0, 0.17)
    elif rev == 2: return 0.26
    else: return False 

def beta1(fc,rev=1):
    if rev   == 1: return P(fc, -1.9972e-05, 2.2655e-04, 8.1748e-02)
    elif rev == 2: return 0.285*pow(fc,-0.94843)
    else: return False 

def theta1(fc,rev=1):
    if   rev == 1: return P(fc, -4.0856E-07, -1.2132E-06, 1.5593E-03)
    elif rev == 2: return 0
    else: return False 

def Q1(fc, J, rev=1): 
    return alpha1(fc,rev)-lamda1(fc,rev)*np.exp(-beta1(fc,rev)*J)+theta1(fc,rev)*J

def TOR(fc, J, rev=1):
    return Q1(fc,J,rev)*TXC(fc,J,rev)

def alpha2(fc,rev=1):
    if rev   == 1: return P(fc, 0, 0, 0.66)
    elif rev == 2: return 0.76
    else: return False 

def lamda2(fc,rev=1):
    if   rev == 1: return P(fc, 0, 0, 0.16)
    elif rev == 2: return 0.26
    else: return False 

def beta2(fc,rev=1):
    if rev   == 1: return P(fc, -1.9972e-05, 2.2655e-04, 8.2748e-02)
    elif rev == 2: return 0.285*pow(fc,-0.94843)
    else: return False 

def theta2(fc,rev=1):
    if   rev == 1: return P(fc, -4.8697e-07, -1.8883e-06, 1.8822e-03)
    elif rev == 2: return 0
    else: return False 

def Q2(fc, J, rev=1):
    return alpha2(fc,rev)-lamda2(fc,rev)*np.exp(-beta2(fc,rev)*J)+theta2(fc,rev)*J

def TXE(fc, J, rev=1):
    return Q2(fc,J,rev)*TXC(fc,J,rev)

def X0(fc,rev=1):
    if rev   == 1: return P(fc, 8.769178e-03, -7.3302306e-02, 84.85)
    elif rev == 2: return 17.087+1.892*fc
    else: return False 

def R(fc,rev=1):
    if rev   == 1: return 5
    elif rev == 2: return 4.45994*np.exp(-fc/11.51679)+1.95358
    else: return False 

def W(fc,rev=1):
    if rev   == 1: return 0.05
    elif rev == 2: return 0.065
    else: return False 

def D1(fc,rev=1):
    if rev   == 1: return 2.5E-4
    elif rev == 2: return 6.11e-4
    else: return False 

def D2(fc,rev=1):
    if rev   == 1: return 3.49E-7
    elif rev == 2: return 2.225E-6
    else: return False 

def plasticVolumetricStrain(fc,X,rev=1):
    return W(fc,rev)*(1-np.exp(-D1(fc,rev)*(X-X0(fc,rev))-D2(fc,rev)*pow(X-X0(fc,rev),2)))

def hydrostaticCompressionParameters(fc,X,rev=1):
    return D1(fc,rev)*(X-X0(fc,rev))+D2(fc,rev)*pow(X-X0(fc,rev),2)

def B(fc,rev=1):
    if rev   == 1: return 100
    elif rev == 2: return False ######
    else: return False 

def D(fc,rev=1):
    if rev   == 1: return 0.1
    elif rev == 2: return False #####
    else: return False 

def eta_t(fc,rev=1): 
    if rev   == 1: return 0.48
    elif rev == 2: return 0
    else: return False 

def eta_0_t(fc,rev=1): 
    fc_in_psi= fc*145.0377
    if rev   == 1: return P(fc_in_psi, 8.0614774E-13, -9.77736719E-10, 5.0752351E-05)
    elif rev == 2: return 0
    else: return False 

def eta_c(fc,rev=1): 
    if rev   == 1: return 0.78
    elif rev == 2: return 0
    else: return False 

def eta_0_c(fc,rev=1):
    fc_in_psi= fc*145.0377
    if rev   == 1: return P(fc_in_psi, 1.2772337E-11, -1.0613722E-07, 3.203497E-4)
    elif rev == 2: return 0
    else: return False

def overt(fc,rev=1): 
    return P(fc, 1.309663E-02, -0.3927659, 21.45)    

def overc(fc,rev=1): 
    return overt(fc,rev=1)

def Q1MC(fc, rev=1):
    return np.sqrt(3)*Q2(fc,rev)/(1+Q2(fc, rev))

def Q2MC(fc, rev=1):
    return TXE(fc, rev=1)/TXC(fc, rev=1)

def Q1WW(fc, rev=1):
    q=(1-pow(Q2(fc, rev),2))
    return (np.sqrt(3)*q+(2*Q2(fc, rev)-1)*np.sqrt((3*q)+5*pow(Q2(fc, rev),2)-4*Q2(fc, rev)))/(3*q+pow(1-2*Q2(fc, rev),2))

def TORMC(fc, J, rev=1):
    return Q1MC(fc,J,rev)*TXC(fc,J,rev)

def TXEMC(fc, rev=1):
    return Q2MC(fc,J,rev)*TXC(fc,J,rev)

def TORWW(fc, J, rev=1):
    return Q1WW(fc,J,rev)*TXC(fc,J,rev)

def printCEBFIP(fc, dmax, rho = 2.4E-9):
    items = CEBFIB(fc, dmax,rho)
    text  = '$#\n'
    text += '$# CEBFIP Estimations:\n'
    for key in items:
        text += '$# {0} = {1:G}\n'.format(key,items[key])
    text += '$#\n'
    return text

def CSCM(
    concreteClass = 30, 
    dmax    = 19, 
    mid     = 159,   
    rho     = 2.4E-9, 
    nplot   = 1,    # maximum of brittle and ductile damage 
    incre   = 0,    # maximum strain increment for subincrementation.
    irate   = 'on', # rate effects model turned on
    erode   = 'off', 
    recov   = 'full',    # the modulus is recovered in compression when RECOV is equal to 0
    itretrc = 0,    # cap does not retract 
    pred    = 'off',    # preexisting damage 
    srate   = 1,    # ratio of effective shear stress to tensile stress fluidity parameters
    repow   = 1,    # power that increases fracture energy with rate effects
    nh      = 0,    # hardening initiation
    ch      = 0,    # hardening rate
    pwrc    = 5,    # shear-to-compression transition parameter
    pwrt    = 1,    # shear-to-tension transition parameter
    pmod    = 0,    # modify moderate pressure softening parameter
    rev = 1
    ):
    #
    if irate == 'on': irate = 1
    elif irate == 'off': irate = 0
    else: print 'Error in ireate'
    #
    if erode == 'off': erode = 0.99
    else: erode = 1+ float(erode)
    #
    if pred == 'off': pred = 0
    else: pred = float(pred)
    #
    if recov == 'full': recov = 0
    else: recov = 1-float(recov)
    #
    data = CEBFIB(concreteClass,dmax)
    CSCM = OD()
    CSCM['NAME']    = '*MAT_CSCM'
    #
    CSCM['MID']     = {'card':1, 'position':1, 'type':'A8', 'value':mid}
    CSCM['RHO']     = {'card':1, 'position':2, 'type':'F',  'value':rho}
    CSCM['NPLOT']   = {'card':1, 'position':3, 'type':'I',  'value':nplot}
    CSCM['INCRE']   = {'card':1, 'position':4, 'type':'F',  'value':incre}
    CSCM['IRATE']   = {'card':1, 'position':5, 'type':'I',  'value':irate}
    CSCM['ERODE']   = {'card':1, 'position':6, 'type':'F',  'value':erode}
    CSCM['RECOV']   = {'card':1, 'position':7, 'type':'F',  'value':recov}
    CSCM['ITRETRC'] = {'card':1, 'position':8, 'type':'I',  'value':itretrc}
    #   
    CSCM['PRED']    = {'card':2, 'position':1, 'type':'F',  'value':pred}
    #
    CSCM['G']       = {'card':3, 'position':1, 'type':'F',  'value':data['G']}
    CSCM['K']       = {'card':3, 'position':2, 'type':'F',  'value':data['K']}
    CSCM['ALPHA']   = {'card':3, 'position':3, 'type':'F',  'value':alpha(data['fc'],rev)}
    CSCM['THETA']   = {'card':3, 'position':4, 'type':'F',  'value':theta(data['fc'],rev)}
    CSCM['LAMBDA']  = {'card':3, 'position':5, 'type':'F',  'value':lamda(data['fc'],rev)}
    CSCM['BETA']    = {'card':3, 'position':6, 'type':'F',  'value': beta(data['fc'],rev)}
    CSCM['NH']      = {'card':3, 'position':7, 'type':'F',  'value':nh}
    CSCM['CH']      = {'card':3, 'position':8, 'type':'F',  'value':ch}
    #
    CSCM['ALPHA1']  = {'card':4, 'position':1, 'type':'F',  'value':alpha1(data['fc'],rev)}
    CSCM['THETA1']  = {'card':4, 'position':2, 'type':'F',  'value':theta1(data['fc'],rev)}
    CSCM['LAMBDA1'] = {'card':4, 'position':3, 'type':'F',  'value':lamda1(data['fc'],rev)}
    CSCM['BETA1']   = {'card':4, 'position':4, 'type':'F',  'value': beta2(data['fc'],rev)}
    CSCM['ALPHA2']  = {'card':4, 'position':5, 'type':'F',  'value':alpha2(data['fc'],rev)}
    CSCM['THETA2']  = {'card':4, 'position':6, 'type':'F',  'value':theta2(data['fc'],rev)}
    CSCM['LAMBDA2'] = {'card':4, 'position':7, 'type':'F',  'value':lamda2(data['fc'],rev)}
    CSCM['BETA2']   = {'card':4, 'position':8, 'type':'F',  'value': beta2(data['fc'],rev)}
    #
    CSCM['R']       = {'card':5, 'position':1, 'type':'F',  'value': R(data['fc'],rev)}
    CSCM['X0']      = {'card':5, 'position':2, 'type':'F',  'value':X0(data['fc'],rev)}
    CSCM['W']       = {'card':5, 'position':3, 'type':'F',  'value': W(data['fc'],rev)}
    CSCM['D1']      = {'card':5, 'position':4, 'type':'F',  'value':D1(data['fc'],rev)}
    CSCM['D2']      = {'card':5, 'position':5, 'type':'F',  'value':D2(data['fc'],rev)}
    #
    CSCM['B']       = {'card':6, 'position':1, 'type':'F',  'value':B(data['fc'],1)}
    CSCM['GFC']     = {'card':6, 'position':2, 'type':'F',  'value':data['Gfc']}
    CSCM['D']       = {'card':6, 'position':3, 'type':'F',  'value':D(data['fc'],1)}
    CSCM['GFT']     = {'card':6, 'position':4, 'type':'F',  'value':data['Gft']}
    CSCM['GFS']     = {'card':6, 'position':5, 'type':'F',  'value':data['Gfs']}
    CSCM['PWRC']    = {'card':6, 'position':6, 'type':'F',  'value':pwrc}
    CSCM['PWRT']    = {'card':6, 'position':7, 'type':'F',  'value':pwrt}
    CSCM['PMOD']    = {'card':6, 'position':8, 'type':'F',  'value':pmod}
    #
    CSCM['ETA_0_C'] = {'card':7, 'position':1, 'type':'F',  'value':eta_0_c(data['fc'],rev)}
    CSCM['ETA_C']   = {'card':7, 'position':2, 'type':'F',  'value':  eta_c(data['fc'],rev)}
    CSCM['ETA_0_T'] = {'card':7, 'position':3, 'type':'F',  'value':eta_0_t(data['fc'],rev)}
    CSCM['ETA_T']   = {'card':7, 'position':4, 'type':'F',  'value':  eta_t(data['fc'],rev)}
    CSCM['OVERC']   = {'card':7, 'position':5, 'type':'F',  'value':  overc(data['fc'],rev)}
    CSCM['OVERT']   = {'card':7, 'position':6, 'type':'F',  'value':  overt(data['fc'],rev)}
    CSCM['SRATE']   = {'card':7, 'position':7, 'type':'F',  'value':srate}
    CSCM['REPOW']   = {'card':7, 'position':8, 'type':'F',  'value':repow}  
    return CSCM

def keyword2text(
    data,             # ordered dict with card data to be processed
    wordLength  = 10, # word lenght in case of dp keyword
    wordNumber  = 8   # word number in card line
    ): 
    emptyCard   = ' '*wordLength*wordNumber
    cardCount   = 0
    planeText = ''
    items = data.keys()[1:]
    keywordText = [data['NAME']]
    for key in items:
        if data[key]['card']>cardCount:
            cardCount = data[key]['card']
            keywordText.append('')
            keywordText.append('')
        if data[key]['position'] == 1: 
            keywordText[2*cardCount-1] += '$#{0: >{1}s}'.format(key,wordLength-2)
        else:                          
            keywordText[2*cardCount-1] +=  ' {0: >{1}s}'.format(key,wordLength-1)
        if data[key]['value'] == 'AUTO':
            keywordText[2*cardCount]   +=   '{0}'.format(' '*wordLength)
        else:
            if data[key]['type']   == 'A8': 
                keywordText[2*cardCount]+=   ' {0:>{1}s}'.format(  str(data[key]['value']),wordLength-1)
            elif data[key]['type'] == 'I':  
                keywordText[2*cardCount]+=   ' {0:>{1}d}'.format(  int(data[key]['value']),wordLength-1)
            elif data[key]['type'] == 'F':  
                keywordText[2*cardCount]+=' {0:{1}.{2}G}'.format(float(data[key]['value']),wordLength-1,wordLength-6)
            else:                           
                keywordText[2*cardCount]+=          '{0}'.format(' '*wordLength)                     
    for lines in keywordText: planeText+=lines+'\n'
    return planeText



fc = 50
dmax = 16.0
rho  = 2.4E-9
rev  = 2
card = keyword2text(CSCM(fc,dmax,irate='on',erode='off', pred='off', recov = 'full', rev=rev)) + printCEBFIP(fc, dmax, rho )


print card
pyperclip.copy(card)