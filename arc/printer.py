#! /usr/binfile/python
# -*- codinfileg: utf-8 -*-
import math
import os
from collections import OrderedDict as OD

data = OD()

data['NAME']    = '*MAT_CDPM'
data['MID']     = {'card':1, 'position':1, 'type':'A8', 'default':273,      'value':False}
data['RHO']     = {'card':1, 'position':2, 'type':'F',  'default':'none',   'value':False}
data['E']       = {'card':1, 'position':3, 'type':'F',  'default':'none',   'value':False}
data['PR']      = {'card':1, 'position':4, 'type':'F',  'default':0.2 ,     'value':False}
data['ECC']     = {'card':1, 'position':5, 'type':'F',  'default':'AUTO',   'value':False}
data['QH0']     = {'card':1, 'position':6, 'type':'F',  'default':0.3 ,     'value':False}
data['FT']      = {'card':1, 'position':7, 'type':'F',  'default':'none',   'value':False}
data['FC']      = {'card':1, 'position':8, 'type':'F',  'default':'none',   'value':False}
data['HP']      = {'card':2, 'position':1, 'type':'F',  'default':0.5,      'value':False}
data['AH']      = {'card':2, 'position':2, 'type':'F',  'default':0.08,     'value':False}
data['BH']      = {'card':2, 'position':3, 'type':'F',  'default':0.003,    'value':False}
data['CH']      = {'card':2, 'position':4, 'type':'F',  'default':2.0,      'value':False}
data['DH']      = {'card':2, 'position':5, 'type':'F',  'default':'AUTO',   'value':False}
data['AS']      = {'card':2, 'position':6, 'type':'F',  'default':1.0E-6,   'value':False}
data['DF']      = {'card':2, 'position':7, 'type':'F',  'default':15.0,     'value':False}
data['FC0']     = {'card':2, 'position':8, 'type':'F',  'default':'AUTO',   'value':False}
data['TYPE']    = {'card':3, 'position':1, 'type':'F',  'default':'0.0',    'value':False}
data['BS']      = {'card':3, 'position':2, 'type':'F',  'default':'1.0',    'value':False}
data['WF']      = {'card':3, 'position':3, 'type':'F',  'default':'none',   'value':False}
data['WF1']     = {'card':3, 'position':4, 'type':'F',  'default':'0.15*WF','value':False}
data['FT1']     = {'card':3, 'position':5, 'type':'F',  'default':'0.3*FT', 'value':False}
data['STRFLG']  = {'card':3, 'position':6, 'type':'F',  'default':'0.0',    'value':False}
data['FAILFLG'] = {'card':3, 'position':7, 'type':'F',  'default':'0.0',    'value':False}
data['EFC']     = {'card':3, 'position':8, 'type':'F',  'default':1.0E-4,   'value':False}


wordLength  = 10
wordNumber  = 8
emptyCard   = ' '*wordNumber*wordNumber
header      = data[0]
items       = data[1:][0]
keywordText = [header]
cardCount   = 1
# count number of cards 
for key in items.keys(): 
    if items[key]['card']> cardCount:
        cardCount = items[key]['card']
# make emply keyword templane with spaces
for i in xrange(cardCount):
        print i
        keywordText.append(emptyCard)
        keywordText.append(emptyCard)

for key in items.keys():
    start = wordLength*(items[key]['position'] - 1)
    end   = wordLength* items[key]['position']
    keywordText[items[key]['card']] = strReplace(keywordText[items[key]['card']], start, end, ' {0: >9s}'.format(key))






i = 1
j = 3
k = 'qwe'
test = test[:i]+ k + test[j:]
print test

    if item.values()[0]['position'] == 1: keywordText[2*currentCard-1] += '$#{0: >8s}'.format(item.keys()[0])
    else:                                 keywordText[2*currentCard-1] +=  ' {0: >9s}'.format(item.keys()[0])
    if item.values()[0]['type'] == 'A8':  keywordText[2*currentCard] +=  ' {0:>9s}'.format(  str(item.values()[0]['value']))
    elif item.values()[0]['type'] == 'I': keywordText[2*currentCard] +=  ' {0:>9d}'.format(  int(item.values()[0]['value']))
    else:                                 keywordText[2*currentCard] += ' {0:8.3e}'.format(float(item.values()[0]['value']))
for i in keywordText: print i
return keywordText