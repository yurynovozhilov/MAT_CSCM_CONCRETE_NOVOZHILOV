#! /usr/binfile/python
# -*- codinfileg: utf-8 -*-
import math
import os
import pyperclip
from collections import OrderedDict as OD
from pint import UnitRegistry
units = UnitRegistry()

def askUser(*values):
    askDic = {
    'rho':          {'default':'2400 kg/m^3','question':'Density?'},
    'fc':           {'default':'40 MPa',     'question':'f\'c?'},
    'erode':        {'default':100,          'question':'Eroding strain limits in %(less then 0 if no erosion)?'},
    'strainrate':   {'default':'y',          'question':'Enable strain rate effects "y"/"n")?'},
    'nu':           {'default':0.15,         'question':'Poison ratio?'},
    'dagg':         {'default':'19 mm',      'question':'Agrigate size?'},
    'pred':         {'default':0,            'question':'Initial damage in %?'},
    'unitSystem':   {'default':1,            'question':'Target units system?\n 1 -  m, kg, N,  Pa\n 2 - mm, Mg, N, MPa'}
    }
    userValues = {}
    for key in values:
        if not key in askDic.keys():
            print 'Internal error: unknown request about "{0}"\n'.format(key)
        else:
            userValues[key] = userInput(askDic.get(key).get('question'),askDic.get(key).get('default'))
    return userValues

def userInput(question, defaultValue):
    while True:
            userValue = inputDefault(question,defaultValue)
            try:
                defaultValueUnits = units(defaultValue.split()[1])
                try:
                    userValueUnits = units(userValue.split()[1])
                    if userValueUnits.dimensionality == defaultValueUnits.dimensionality: 
                        userValueQuantity = float(userValue.split()[0])
                        return userValueQuantity*userValueUnits 
                    else: 
                        print 'Wrang input dimensionality: user input {0} is not expected {1}\n'.format(userValueUnits.dimensionality, defaultValueUnits.dimensionality)
                except:
                    print 'Wrang input syntax: cannot find units or dimensionless input. Try again please.\n' 
            except:
                userValueType       = type(userValue)
                defaultValueType    = type(defaultValue)
                if  (defaultValueType != str and userValueType != str) or (defaultValueType == str and userValueType == str): 
                    return userValue
                else: 
                    print ('Wrang input type: user input {0} is not expected {1}\n'.format(userValueType,defaultValueType))

def isDimensional(value):
    try:
        value.dimensionality
        return True
    except:
        return False

def inputDefault(question,defaultValue): 
    value = raw_input('{0}\nDefault value is [{1}]\n'.format(question,defaultValue)) or defaultValue
    try:    return float(value)
    except: return value

def setDefault(dic):
    if not dic['value']: 
        dic['value'] = dic['default']
    return dic

def CDPMspecialData(defaultData):
    data = {}
    data['TYPE'] = 2.0
    tetraMesh = False
    ################################################
    # MAT_CONCRETE_DAMAGE_PLASTIC_MODEL stecial data
    #  Tensile softening branch for exponential tensile damage formulation
    WFexp = defaultData['fracture energy']/defaultData['tensile strenght']
    '''
    TYPE=0 (linear softening), WF = 2 GF/FT 
    TYPE=1 (bilinear softening), WF = 4.444 GF/FT. 
    TYPE=2 (exponential softening), WF = GF/FT.
    For tetrahedral meshes it is currently recommended to use 0.56 WF because the way that the element length is computed for this type of element overestimates the fracture energy.
    '''
    if   int(data['TYPE']) == 0: data['tensile threshold'] = WFexp*2
    elif int(data['TYPE']) == 1: data['tensile threshold'] = WFexp*4.444
    elif int(data['TYPE']) == 2: data['tensile threshold'] = WFexp
    else: print 'Wrong TYPE of tensile threshold'
    if tetraMesh: data['tensile threshold'] *= 0.56
    return data

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
    Gf      = Gf0*pow(fcm/fcm0, 0.7)/1e-3
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
    return data

def CDPMgenerate():
    CDPM = OD()
    CDPM['NAME']    = '*MAT_CDPM'
    CDPM['MID']     = {'card':1, 'position':1, 'type':'A8', 'default':273,      'value':False, 'quantity':False}
    CDPM['RHO']     = {'card':1, 'position':2, 'type':'F',  'default':'none',   'value':False, 'quantity':'density'}
    CDPM['E']       = {'card':1, 'position':3, 'type':'F',  'default':'none',   'value':False, 'quantity':'elasticity modulus'}
    CDPM['PR']      = {'card':1, 'position':4, 'type':'F',  'default':0.2 ,     'value':False, 'quantity':'poisson ratio'}
    CDPM['ECC']     = {'card':1, 'position':5, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False }
    CDPM['QH0']     = {'card':1, 'position':6, 'type':'F',  'default':0.3 ,     'value':False, 'quantity':False }
    CDPM['FT']      = {'card':1, 'position':7, 'type':'F',  'default':'none',   'value':False, 'quantity':'tensile strenght'}
    CDPM['FC']      = {'card':1, 'position':8, 'type':'F',  'default':'none',   'value':False, 'quantity':'compressive strength'}
    CDPM['HP']      = {'card':2, 'position':1, 'type':'F',  'default':0.5,      'value':False, 'quantity':False}
    CDPM['AH']      = {'card':2, 'position':2, 'type':'F',  'default':0.08,     'value':False, 'quantity':False}
    CDPM['BH']      = {'card':2, 'position':3, 'type':'F',  'default':0.003,    'value':False, 'quantity':False}
    CDPM['CH']      = {'card':2, 'position':4, 'type':'F',  'default':2.0,      'value':False, 'quantity':False}
    CDPM['DH']      = {'card':2, 'position':5, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['AS']      = {'card':2, 'position':6, 'type':'F',  'default':1.0E-6,   'value':False, 'quantity':False}
    CDPM['DF']      = {'card':2, 'position':7, 'type':'F',  'default':15.0,     'value':False, 'quantity':False}
    CDPM['FC0']     = {'card':2, 'position':8, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['TYPE']    = {'card':3, 'position':1, 'type':'F',  'default':'0.0',    'value':False, 'quantity':'TYPE'}
    CDPM['BS']      = {'card':3, 'position':2, 'type':'F',  'default':'1.0',    'value':False, 'quantity':False}
    CDPM['WF']      = {'card':3, 'position':3, 'type':'F',  'default':'none',   'value':False, 'quantity':'tensile threshold'}
    CDPM['WF1']     = {'card':3, 'position':4, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['FT1']     = {'card':3, 'position':5, 'type':'F',  'default':'AUTO',   'value':False, 'quantity':False}
    CDPM['STRFLG']  = {'card':3, 'position':6, 'type':'F',  'default':'0.0',    'value':False, 'quantity':False}
    CDPM['FAILFLG'] = {'card':3, 'position':7, 'type':'F',  'default':'0.0',    'value':False, 'quantity':False}
    CDPM['EFC']     = {'card':3, 'position':8, 'type':'F',  'default':1.0E-4,   'value':False, 'quantity':False}
    return CDPM

def CDPMfit(fc, rho, dmax):
    CDPM = CDPMgenerate()
    data = {}
    data.update(CEBFIB(fc, rho, dmax))
    data.update(CDPMspecialData(data))
    items = CDPM.keys()[1:]
    for key in items:
        if not CDPM[key]['quantity']:
            if CDPM[key]['default'] == 'AUTO': 
                CDPM[key]['value']=0
            else:
                CDPM[key]['value']=CDPM[key]['default']       
        else:
            CDPM[key]['value']=data[CDPM[key]['quantity']]
    '''
    CDPM['RHO']['value']  = data['density']
    CDPM['E']['value']    = data['elasticity modulus']
    CDPM['PR']['value']   = data['poisson ratio'] 
    CDPM['FT']['value']   = data['tensile strenght']    
    CDPM['FC']['value']   = data['compressive strength']
    CDPM['TYPE']['value'] = 1.0
    '''
    '''
    if   int(CDPM['TYPE']['value']) == 0: CDPM['WF']['value'] = data['fractureEnergy']/data['tensileStrenght']*2
    elif int(CDPM['TYPE']['value']) == 1: CDPM['WF']['value'] = data['fractureEnergy']/data['tensileStrenght']*4.444
    elif int(CDPM['TYPE']['value']) == 3: CDPM['WF']['value'] = data['fractureEnergy']/data['tensileStrenght']
    else: CDPM['WF']['value'] = 0.0
    
    '''
    return CDPM

def keyword2text(data):
    wordLength  = 10
    wordNumber  = 8
    emptyCard   = ' '*wordNumber*wordNumber
    cardCount   = 0
    items = data.keys()[1:]
    keywordText = [data['NAME']]
    for key in items:
        if data[key]['card']> cardCount:
            cardCount = data[key]['card']
            keywordText.append('')
            keywordText.append('')
        if data[key]['position'] == 1: keywordText[2*cardCount-1] += '$#{0: >8s}'.format(key)
        else:                          keywordText[2*cardCount-1] +=  ' {0: >9s}'.format(key)
        if data[key]['type'] == 'A8':  keywordText[2*cardCount]   +=   ' {0:>9s}'.format(  str(data[key]['value']))
        elif data[key]['type'] == 'I': keywordText[2*cardCount]   +=   ' {0:>9d}'.format(  int(data[key]['value']))
        else:                          keywordText[2*cardCount]   +=  ' {0:8.3e}'.format(float(data[key]['value']))
    planeText = ''
    for lines in keywordText: 
        print lines
        planeText +=lines + '\n'
    return planeText

pyperclip.copy(keyword2text(CDPMfit(40, 2.4E-9, 16)))



