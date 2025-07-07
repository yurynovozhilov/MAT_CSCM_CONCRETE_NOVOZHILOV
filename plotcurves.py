import numpy as np
import matplotlib.pyplot as plt

def plotStile(**features):
    stile = dict()
    #
    stile['fontsize'] = 18
    #
    stile['imgSizeXinches'] = 15
    stile['imgSizeYinches'] = 10
    #
    stile['xLimBottom'] = False
    stile['xLimTop']    = False
    stile['yLimBottom'] = False
    stile['yLimTop']    = False
    #
    stile['title']  = ''
    stile['xLabel'] = ''
    stile['yLabel'] = ''
    #
    stile['xScale'] = 'linear'
    stile['yScale'] = 'linear'
    #
    stile['legendLocation'] = 'best'
    #
    for key, value in features.items():
        if key in stile.keys(): 
            stile[key] = value
        else:
            print('Wrong option {0}'.format(key))
    if type(stile['xLimBottom'])==bool or stile['xLimTop']==bool:
        del stile['xLimBottom']
        del stile['xLimTop']
    if type(stile['yLimBottom'])==bool or stile['yLimTop']==bool:
        del stile['yLimBottom']
        del stile['yLimTop']
    return stile

def plot(stile, *curves):
    # set plot size
    plt.figure(figsize=(stile['imgSizeXinches'], stile['imgSizeYinches']))
    # define curves
    for dataset in curves:
        plt.plot(
            dataset['array'][0], 
            dataset['array'][1],
            label      = dataset['lable'], 
            color      = dataset['color'],
            linestyle  = dataset['linestyle'],
            linewidth  = dataset['linewidth'],
        )       
    # axis font size
    plt.tick_params(labelsize = stile['fontsize'])
    
    # legend position and font size
    plt.legend(loc=stile['legendLocation'],prop={'size':stile['fontsize']})
    # axis lables 
    plt.xlabel(stile['xLabel']).set_fontsize(stile['fontsize']+2)
    plt.ylabel(stile['yLabel']).set_fontsize(stile['fontsize']+2)
    # title
    plt.title(stile['title']).set_fontsize(stile['fontsize']+4)
    # grid
    plt.grid(True)
    # axis scale
    plt.xscale(stile['xScale'])   
    plt.yscale(stile['yScale'])
    # scope for axis: if no scope in input then use auto scope
    if 'xLimBottom' in stile.keys() and 'xLimTop' in stile.keys():
        plt.xlim(stile['xLimBottom'],stile['xLimTop'])
    if 'yLimBottom' in stile.keys() and 'yLimTop' in stile.keys():
        plt.ylim(stile['yLimBottom'],stile['yLimTop'])
    # visualisation
    plt.show()
    return


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

def plotSingleCurve (
    x, 
    y,
    title,
    xLabel, 
    yLabel 
):
    
    fontsize=18
    linewidth=2.0
    imgSizeYinches=10
    imgSizeXinches=15
 
    fig = plt.figure()
    ax  = fig.add_subplot(111)
    fig.set_size_inches(imgSizeXinches, imgSizeYinches, forward=True)
    
    ax.grid(True)
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.plot(x, y, color='blue',linewidth=2.0)
    
    plt.xlabel(xLabel).set_fontsize(fontsize+2)
    plt.ylabel(yLabel).set_fontsize(fontsize+2)
    plt.title(title).set_fontsize(fontsize+4)
    
    plt.show()
    
   # np.savetxt("stress-strein uncofiend compression curve.csv", np.vstack((epsilon_c, sigma_c)).transpose(), delimiter=",")
    return

def plotTwoCurves(
    x,
    y1,
    y2,
    title  = '',
    label1 ='rev 1', 
    label2 ='rev 2', 
    xLabel ='Ox',
    yLabel ='Oy'
):

    fontsize=18
    linewidth=2.0
    imgSizeYinches=10
    imgSizeXinches=15

    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    fig.set_size_inches(imgSizeXinches, imgSizeYinches, forward=True)

    ax.plot(x, y1, label = label1, color='blue',linewidth=2.0)
    ax.plot(x, y2, label = label2, color='red',linewidth=2.0)

    ax.grid(True)
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    
#    ax.set_xlim([xlim_0,xlim_1])
#    ax.set_ylim([ylim_0,ylim_1])
    
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.xaxis.set_ticks_position('bottom')
    ax.spines['bottom'].set_position(('data',0))

    ax.yaxis.set_ticks_position('left')
    ax.spines['left'].set_position(('data',0))

    for label in ax.xaxis.get_ticklabels(): label.set_fontsize(fontsize)
    for label in ax.yaxis.get_ticklabels(): label.set_fontsize(fontsize)

    plt.legend(loc='upper left',prop={'size':fontsize+2})
    plt.xlabel(xLabel).set_fontsize(fontsize+2)
    plt.ylabel(yLabel).set_fontsize(fontsize+2)
    plt.title(title).set_fontsize(fontsize+4)
    
    plt.show()
    return 