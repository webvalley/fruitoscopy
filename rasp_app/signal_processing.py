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

def save_plot(array):
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
    plt.plot(array,c='black');
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
    img_spectrum = im.load()
    return img_spectrum

def get_baseline(img_spectrum, param):
    """
    This function receive as input the matrix of the pixels of the spectrum image, after being cropped, and some parameters as a tuple.
    The return value is the spectra.
    
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
    :value 0: List of y elements of the spectra
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
    :value 1: List of y elements of the spectra
    
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
        
    try:
        almost_good = sps.savgol_filter(black_line, 41, 2)
        
        min_height = min(almost_good)
        
        normalized =  np.array(almost_good)
        normalized -= min_height
        
        try:
            save_plot(normalized)
        except:
            print("Unable to process plot")
        return (0,normalized)
    except:
        print("Unable to save image")
        return 0