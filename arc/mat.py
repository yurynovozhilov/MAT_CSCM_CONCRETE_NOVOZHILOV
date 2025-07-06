#! /usr/binfile/python
# -*- codinfileg: utf-8 -*-
import math
import os
import pyperclip
from collections import OrderedDict as OD
from pint import UnitRegistry
units = UnitRegistry()

def CEBFIB(fc, rho, dmax):
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
        fctm = 2.12*math.log(1+0.1*(fck+delta_f))
    # lower bounds for characteristic tensile strenght
    fck_min = 0.7*fctm
    # upper bounds for characteristic tensile strenght
    fck_max = 1.3*fctm
    # uniaxial tensile strenght
    ft      = fctm
    # biaxial tensile strength
    fbt     = ft
    ################################################
    # Fracture energy
    # (CEB-FIB Model Code 2010 5.1.5.2)             
    # Gf = 73*pow(fcm,0.18) # fracture energy
    # MPa
    fcm0    = 10.0                                  
    # Base value for fracture energy, Nmm/mm^2
    Gf0     = 0.021+5.357E-4*dmax
    # Fracture energy, Nmm/mm^2
    Gf      = Gf0*pow(fcm/fcm0, 0.7)
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
    if not(alpha_i <= 1.0): alpha_i = 1.0
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
    #  Tensile softening branch for exponential tensile damage formulation
    WF  = Gf/ft
    ksi = ft*(fbc**2-fc**2)/(fbc*(fc**2-ft**2))
    ECC = (1+ksi)/(1-ksi)
    ################################################
    # Record data from CEB-FIB estimations
    data = {}
    data['density']                      = rho  
    data['compressive strength']         = fc   
    data['aggregate size']               = dmax 
    data['mean compressive strength']    = fcm   
    data['tensile strenght']             = ft     
    data['biaxial compression strength'] = fbc   
    data['fracture energy']              = Gf     
    data['poisson ratio']                = nu     
    data['elasticity modulus']           = E       
    data['shear modulus']                = G       
    data['bulk modulus']                 = K 
    data['tensile threshold']            = WF
    data['eccentricity parameter']       = ECC
    for key in data:
        print '{0} = {1}'.format(key.capitalize(), data[key])
    return data

def defaultCDPM():
    CDPM = OD()
    CDPM['NAME']    = '*MAT_CDPM'
    CDPM['MID']     = {'card':1, 'position':1, 'type':'A8', 'default':273,      'value':False, 'quantity':False}
    CDPM['RHO']     = {'card':1, 'position':2, 'type':'F',  'default':'none',   'value':False, 'quantity':'density'}
    CDPM['E']       = {'card':1, 'position':3, 'type':'F',  'default':'none',   'value':False, 'quantity':'elasticity modulus'}
    CDPM['PR']      = {'card':1, 'position':4, 'type':'F',  'default':0.2 ,     'value':False, 'quantity':'poisson ratio'}
    CDPM['ECC']     = {'card':1, 'position':5, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False }
    CDPM['QH0']     = {'card':1, 'position':6, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False }
    CDPM['FT']      = {'card':1, 'position':7, 'type':'F',  'default':'none',   'value':False, 'quantity':'tensile strenght'}
    CDPM['FC']      = {'card':1, 'position':8, 'type':'F',  'default':'none',   'value':False, 'quantity':'compressive strength'}
    CDPM['HP']      = {'card':2, 'position':1, 'type':'F',  'default':0.01,     'value':False, 'quantity':False}
    CDPM['AH']      = {'card':2, 'position':2, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['BH']      = {'card':2, 'position':3, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['CH']      = {'card':2, 'position':4, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['DH']      = {'card':2, 'position':5, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['AS']      = {'card':2, 'position':6, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['DF']      = {'card':2, 'position':7, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['FC0']     = {'card':2, 'position':8, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['TYPE']    = {'card':3, 'position':1, 'type':'F',  'default':'0.0',    'value':False, 'quantity':False}
    CDPM['BS']      = {'card':3, 'position':2, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['WF']      = {'card':3, 'position':3, 'type':'F',  'default':'none',   'value':False, 'quantity':'tensile threshold'}
    CDPM['WF1']     = {'card':3, 'position':4, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['FT1']     = {'card':3, 'position':5, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['STRFLG']  = {'card':3, 'position':6, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['FAILFLG'] = {'card':3, 'position':7, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['EFC']     = {'card':3, 'position':8, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    return CDPM

def tuneCDPM(fc, rho, dmax):
    tetraMesh    = False
    CDPM         = defaultCDPM()
    materialData = CEBFIB(fc, rho, dmax)
    items        = CDPM.keys()[1:]
    CDPM['TYPE']['value'] = 2.0
    for key in items:
        if not CDPM[key]['value']:
            if CDPM[key]['quantity']: CDPM[key]['value']=materialData[CDPM[key]['quantity']]
            else:                     CDPM[key]['value']=CDPM[key]['default']            
    '''
    TYPE=0 (linear softening), WF = 2 GF/FT 
    TYPE=1 (bilinear softening), WF = 4.444 GF/FT. 
    TYPE=2 (exponential softening), WF = GF/FT.
    TYPE=3 (no damage)
    For tetrahedral meshes it is currently recommended to use 0.56 WF because the way that the element length is computed for this type of element overestimates the fracture energy.
    '''
    if   int(CDPM['TYPE']['value']) == 0: CDPM['WF']['value']*=2
    elif int(CDPM['TYPE']['value']) == 1: CDPM['WF']['value']*=4.444
    elif int(CDPM['TYPE']['value']) == 2: CDPM['EFC']['value']=1.0E-4
    if tetraMesh: CDPM['WF']['value']*=0.56
    # scecial data
    strainRait = True
    erosionEps = -1
    if strainRait: 
        CDPM['STRFLG']['value']  = 1
        CDPM['HP']['value'] = 0.5
        CDPM['FC0']['value'] = 10.0
    else:
        CDPM['STRFLG']['value']  = 0
        CDPM['HP']['value'] = 0.01
    if erosionEps <= 0:
        CDPM['FAILFLG']['value'] = 0
    else:
        CDPM['FAILFLG']['value'] = erosionEps
    return CDPM

def keyword2text(data):
    wordLength  = 10
    wordNumber  = 8
    emptyCard   = ' '*wordLength*wordNumber
    cardCount   = 0
    items = data.keys()[1:]
    keywordText = [data['NAME']]
    for key in items:
        if data[key]['card']> cardCount:
            cardCount = data[key]['card']
            keywordText.append('')
            keywordText.append('')
        if data[key]['position'] == 1: keywordText[2*cardCount-1] += '$#{0: >{1}s}'.format(key,wordLength-2)
        else:                          keywordText[2*cardCount-1] +=  ' {0: >{1}s}'.format(key,wordLength-1)
        if data[key]['value'] == 'AUTO':
            keywordText[2*cardCount]   +=   '{0}'.format(' '*wordLength)
        else:
            if data[key]['type'] == 'A8':  keywordText[2*cardCount]+= ' {0:>{1}s}'.format(  str(data[key]['value']),wordLength-1)
            elif data[key]['type'] == 'I': keywordText[2*cardCount]+= ' {0:>{1}d}'.format(  int(data[key]['value']),wordLength-1)
            else:                          keywordText[2*cardCount]+=' {0:{1}.3e}'.format(float(data[key]['value']),wordLength-2)
    planeText = ''
    for lines in keywordText: 
        print lines
        planeText +=lines + '\n'
    return planeText

pyperclip.copy(keyword2text(tuneCDPM(23.5, 2.4E-9, 10)))



