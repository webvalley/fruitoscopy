import matplotlib.pyplot as plt
import numpy as np
import os
from scipy import signal
import argparse
import sys

# Generate a sliding window of wl dimension
def win_iter(l, wl = 5):
    ss = l // wl
    splits = np.array_split(np.arange(l), ss)
    for s in splits:
        yield s


# Reduces noise in a 2-step process.
def remove_noise(arr_0):
    arr_1 = signal.detrend(arr_0)
    arr_2 = signal.savgol_filter(arr_1, 51, 3)
    return arr_2


# Finds mins in the spectra
def mins(array):
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
    

# Remove background from spectra
def remove_background(spectrum, wl, idx, deg):
    # Compute a regression line for the first sample
    p2 = np.polyfit(wl[idx], spectrum[0, idx].flatten(), deg = 3)

    # Calculate the background values
    back_val = []
    print (wl)
    for x in wl:
        back_val_current = 0
        for i in range(len(p2)):
            back_val_current += p2[len(p2) - i - 1]*(x**i)
        back_val.append(back_val_current)

    spec_final = spectrum[0, :] - back_val[0:]
    min_val = np.amin(spec_final)
    for i in range(len(spec_final)):
        spec_final[i] -= min_val

    pf = np.poly1d(p2)
    return [spec_final, pf]


if __name__ == '__main__':
    # read command line args
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required = True, help = 'Name of file.')
    name = vars(parser.parse_args(sys.argv[1:]))['name']

    # Set the working directory
    prjdir = '.'

    # Read the data from a csv file. Columns separated by ','.
    # The first line of the file contains the scanned wavelengths
    tmpdata = np.loadtxt(os.path.join(prjdir, name), delimiter=',')
    wl = tmpdata[0]
    spectrum = tmpdata[1:]

    # Get dataset dimension
    n, p = spectrum.shape
   
    # Have a first look at our spectra
    for i in range(n):
        plt.plot(wl, spectrum[i, :], '--', label='sample %d' % i)
    plt.grid()
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Reflection intensity')
    plt.show()

    # Remove noise
    tmpdata_no_noise = remove_noise(tmpdata)
    wl = tmpdata[0]
    spectrum = tmpdata[1:]

    # Find local minima
    idx = mins(spectrum[0])

    # Remove background
    background_rem = remove_background(spectrum, wl, idx, deg = 3)
    spectra_final = background_rem[0]
    pf = background_rem[1]

    # Plot and have a look at the data
    plt.plot(wl, spectra_final, 'b', label='sample %d' % 0)
    plt.plot(wl[idx], spectrum[0, idx], 'or', label='local minima')
    plt.plot(wl, pf(wl), '--', label='Fitting')
        
    plt.grid()
    plt.legend()
    plt.show()
