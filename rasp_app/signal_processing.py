import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
from signal_processing import *
import scipy.signal as sps
from matplotlib.pylab import savefig
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def mins(array,wl):
    """
    This function receive as input the spectrum and the wavelenghts.
    The return value is the list of the minima.
    
    The purpose of this function is to find the minima of the
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Variables in input:
    ----------
    :param 0: array of the spectrum
    :param 1: list of wavelenghts
    
    
    :Return values:
    ----------
    :value 0: List of minimas of the spectrum
    """
    der = np.diff(array)
    
    prev = 0
    min_vals = []
    for x in range(len(wl)):
        if der[x-1] > 0 and prev < 0:
            min_vals.append(x-1)
        elif der[x-1] == 0 and prev < 0:
            min_vals.append(x-1)
        prev = der[x-1]
    return min_vals

def remove_background(spectrum, wl=[], idx=[], deg=1):
    """
    This function receive as input the spectrum, the wavelenghts, the minima points and the deg to compute the regression line.
    The return value is the label and the normalized spectrum
    
    The purpose of this function is to normalize the spectrum
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Variables in input:
    ----------
    :param 0: array of the spectrum
    :param 1: list of wavelenghts
    :param 2: list of minimas
    :param 3: deg of regression line
    
    :Return values:
    ----------
    :value 0: Normalized spectrum (nparray)
    :value 0: Label of the spectrum
    """
    #This has been disabled because is not the right approach, the regression line is jost a background line,
    #with m = 0
    '''
    # Compute a regression line for the first sample
    p2 = np.polyfit(wl, spectrum, deg = 1)
    
    # Calculate the background values
    back_val = []
    for x in wl:
        back_val_current = 0
        for i in range(len(p2)):
            back_val_current += p2[len(p2) - i - 1]*(x**i)
        back_val.append(back_val_current)

    spec_final = spectrum - back_val
    min_val = np.amin(spec_final)
    for i in range(len(spec_final)):
        spec_final[i] -= min_val

    pf = np.poly1d(p2)
    return [spec_final, pf]
    '''
    min_height = min(spectrum)
    
    normalized =  np.array(spectrum)
    normalized -= min_height
    return (normalized,0)

def save_plot(array, wl=[]):
    """
    This function receive as input an array.
    The return is nothing.
    
    The purpose of this function is to create a plot of the values of the array and save it.
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Values in input:
    ----------
    :value 0: array of the y elements of a spectrum
    
    :Return values:
    ----------
    - no return values
    """
    if wl == []:
        wl = range(len(array))
    plt.clf();plt.plot(array,c='black')
    savefig(HOME_PATH + '/static/spectrum.png', bbox_inches='tight')

def get_image(param):
    """
    This function receive as input some parameters as a tuple.
    The return value is the image of the spectrum.
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Parameters of the tuple:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)
    
    :Return values:
    ----------
    :value 0: Image of the spectrum
    """
    
    im=Image.open(HOME_PATH + '/source.jpg')
    im=im.rotate(param[4])
    im = im.crop(box=param[:4])
    #im.show()
    img_spectrum = im.load()
    return img_spectrum

def get_baseline(img_spectrum, param):
    """
    This function receive as input the matrix of the pixels of the spectrum image, after being cropped, and some parameters as a tuple.
    The return value is the spectrum.
    
    The purpose of this function is to calculate the y values of the spectrum from the image
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Parameters of the tuple:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)
    
    :Matrix:
    ----------
    r,g,b = matrix[col, row]
    where "col" is column of the matrix and "row" is the row
    r, g and b are the 3 components, red, green and blue of every pixel of the matrix
    
    :Return values:
    ----------
    :value 0: List of y elements of the spectrum
    """
    
    rl=np.zeros(param[2]-param[0]);gl=np.zeros(param[2]-param[0]);bl=np.zeros(param[2]-param[0]); 
    for col in range(0,param[2]-param[0],1):
        count=[0.,0.,0.]
        for row in range(0,param[3]-param[1],1):
            #b,g,r = img_spectrum[row,col]
            r,g,b = img_spectrum[col,row]
            if b>10:
                bl[col]+=b/255.
                count[0]+=1.
            if g>10:
                gl[col]+=g/255.
                count[1]+=1.
            if r>10:
                rl[col]+=r/255.
                count[2]+=1.
        if count[2]>0.:
            rl[col]=rl[col]/count[2]
        if count[1]>0.:
            gl[col]=gl[col]/count[1]
        if count[0]>0.:
            bl[col]=bl[col]/count[0]
        '''
        if(col != 0):
            rl[col-1] = rl[col]
            gl[col-1] = gl[col]
            bl[col-1] = bl[col]
        
        if(col == param[2]-param[0]-2):
            rl[col+1] = rl[col]
            gl[col+1] = gl[col]
            bl[col+1] = bl[col]
        '''
    black_line = [round((rl[i]+gl[i]+bl[i])/3.,4) for i in range(len(rl))]
    return black_line

def process_image():
    """
    I will process the image, taking 1 tuple made of parameters as input.
    The return values will be the label of the sample and the spectrum
    
    Specifically:
    @@@@@@@@@@@@@
    
    :Parameters:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)
    
    :Return values:
    ----------
    :value 0: Label of the fruit
    :value 1: List of y elements of the spectrum
    
    """
    
    param = (800,1000,2400,1250,5) #left,top,right,bottom, rotate
    try:
        img_spectrum = get_image(param)
    except:
        print("Unable to get image from source")
        return 0

    try:
        black_line = get_baseline(img_spectrum,param)
    except:
        print("Unable to calculate baseline")
        return 0
        
    almost_good = sps.detrend(black_line)
    almost_good = sps.savgol_filter(black_line, 51, 3)
    
    wl = np.array(range(len(almost_good)))
    idx = mins(almost_good,wl)
    
    background_rem,fn = remove_background(almost_good, wl, idx, deg = 3)
    
    try:
        save_plot(background_rem, wl)
    except:
        print("Unable to process plot")
    return (0,background_rem)
    #except:
       #print("Unable to save image")
        #return 0