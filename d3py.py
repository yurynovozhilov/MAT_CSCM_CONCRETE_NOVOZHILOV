import numpy as np
from CEB import *
from CapModel import *

def CSCM(
    f_c     = 35,
    dmax    = 19, 
    mid     = 159,   
    rho     = 2.4E-9, 
    nplot   = 1,      # maximum of brittle and ductile damage 
    incre   = 0,      # maximum strain increment for subincrementation.
    irate   = 'on',   # rate effects model turned on
    erode   = 'off', 
    recov   = 'full', # the modulus is recovered in compression when RECOV is equal to 0
    itretrc = 0,      # cap does not retract 
    pred    = 'off',  # preexisting damage 
    repow   = 1,      # power that increases fracture energy with rate effects
    nh      = 0,      # hardening initiation
    ch      = 0,      # hardening rate
    pwrc    = 5,      # shear-to-compression transition parameter
    pwrt    = 1,      # shear-to-tension transition parameter
    pmod    = 0       # modify moderate pressure softening parameter
    ):
    # plug
    esize = 200 
    #
    if irate == 'on': 
        irate = 1
    elif irate == 'off': 
        irate = 0
    else:
        print("Error in ireate")
    #
    if erode == 'off': 
        erode = 0.99
    else: 
        erode = 1 + float(erode)
    #
    if pred == 'off': 
        pred = 0
    else: 
        pred = float(pred)
    #
    if recov == 'full': 
        recov = 0
    else: 
        recov = 1-float(recov)
    #
    data = CEB(f_c = f_c, d_max = dmax)
    CSCM = {}
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
    CSCM['ALPHA']   = {'card':3, 'position':3, 'type':'F',  'value':alpha(data['f_c'],2)}
    CSCM['THETA']   = {'card':3, 'position':4, 'type':'F',  'value':theta(data['f_c'],2)}
    CSCM['LAMBDA']  = {'card':3, 'position':5, 'type':'F',  'value':lamda(data['f_c'],2)}
    CSCM['BETA']    = {'card':3, 'position':6, 'type':'F',  'value': beta(data['f_c'],2)}
    CSCM['NH']      = {'card':3, 'position':7, 'type':'F',  'value':nh}
    CSCM['CH']      = {'card':3, 'position':8, 'type':'F',  'value':ch}
    #
    CSCM['ALPHA1']  = {'card':4, 'position':1, 'type':'F',  'value':alpha_1(data['f_c'],2)}
    CSCM['THETA1']  = {'card':4, 'position':2, 'type':'F',  'value':theta_1(data['f_c'],2)}
    CSCM['LAMBDA1'] = {'card':4, 'position':3, 'type':'F',  'value':lamda_1(data['f_c'],2)}
    CSCM['BETA1']   = {'card':4, 'position':4, 'type':'F',  'value': beta_1(data['f_c'],2)}
    CSCM['ALPHA2']  = {'card':4, 'position':5, 'type':'F',  'value':alpha_2(data['f_c'],2)}
    CSCM['THETA2']  = {'card':4, 'position':6, 'type':'F',  'value':theta_2(data['f_c'],2)}
    CSCM['LAMBDA2'] = {'card':4, 'position':7, 'type':'F',  'value':lamda_2(data['f_c'],2)}
    CSCM['BETA2']   = {'card':4, 'position':8, 'type':'F',  'value': beta_2(data['f_c'],2)}
    #
    CSCM['R']       = {'card':5, 'position':1, 'type':'F',  'value':  R(data['f_c'],2)}
    CSCM['X0']      = {'card':5, 'position':2, 'type':'F',  'value': X0(data['f_c'],2)}
    CSCM['W']       = {'card':5, 'position':3, 'type':'F',  'value':  W(data['f_c'],2)}
    CSCM['D1']      = {'card':5, 'position':4, 'type':'F',  'value':D_1(data['f_c'],2)}
    CSCM['D2']      = {'card':5, 'position':5, 'type':'F',  'value':D_2(data['f_c'],2)}
    #
    CSCM['B']       = {'card':6, 'position':1, 'type':'F',  'value':B(data['f_c'],data['E'],data['G_fc'],esize,1)}
    CSCM['GFC']     = {'card':6, 'position':2, 'type':'F',  'value':data['G_fc']}
    CSCM['D']       = {'card':6, 'position':3, 'type':'F',  'value':D(data['f_t'],data['E'],data['G_ft'],esize,1)}
    CSCM['GFT']     = {'card':6, 'position':4, 'type':'F',  'value':data['G_ft']}
    CSCM['GFS']     = {'card':6, 'position':5, 'type':'F',  'value':data['G_fs']}
    CSCM['PWRC']    = {'card':6, 'position':6, 'type':'F',  'value':pwrc}
    CSCM['PWRT']    = {'card':6, 'position':7, 'type':'F',  'value':pwrt}
    CSCM['PMOD']    = {'card':6, 'position':8, 'type':'F',  'value':pmod}
    #
    CSCM['ETA_0_C'] = {'card':7, 'position':1, 'type':'F',  'value':eta_0_c(data['f_c'],1)}
    CSCM['N_C']     = {'card':7, 'position':2, 'type':'F',  'value':    n_c(data['f_c'],1)}
    CSCM['ETA_0_T'] = {'card':7, 'position':3, 'type':'F',  'value':eta_0_t(data['f_c'],1)}
    CSCM['N_T']     = {'card':7, 'position':4, 'type':'F',  'value':    n_t(data['f_c'],1)}
    CSCM['OVERC']   = {'card':7, 'position':5, 'type':'F',  'value':  overc(data['f_c'],1)}
    CSCM['OVERT']   = {'card':7, 'position':6, 'type':'F',  'value':  overt(data['f_c'],1)}
    CSCM['SRATE']   = {'card':7, 'position':7, 'type':'F',  'value':  Srate(data['f_c'],1)}
    CSCM['REPOW']   = {'card':7, 'position':8, 'type':'F',  'value':repow}  
    return CSCM

def CEBout(f_c, dmax, rho = 2.4E-9):
    items = CEB(f_c,dmax,rho)
    text  = '$#\n'
    text += '$# CEBFIP Estimations:\n'
    for key in items:
        if type(items[key]) != np.ndarray:
            text += '$# {0} = {1:G}\n'.format(key,items[key])
    text += '$#\n'
    return text

def keyword2text(
    data,             # ordered dict with card data to be processed
    wordLength  = 10, # word lenght in case of dp keyword
    wordNumber  = 8   # word number in card line
    ): 
    emptyCard   = ' '*wordLength*wordNumber
    cardCount   = 0
    planeText   = ''
    items = list(data.keys())[1:]
    keywordText = [data['NAME']]
    for key in items:
        if int(data[key]['card'])>cardCount:
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