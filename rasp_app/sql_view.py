import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.signal as sps
import sqlite3 as sqlite
import time

if __name__ == '__main__':

    # Set the working directory
    prjdir = '' #Current directory

    # Read the data from a csv file. Columns separated by \t.
    # The first line of the file contains the scanned wavelengths
    millis = int(round(time.time() * 1000))
    con = sqlite.connect('samples.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Samples")
    con.commit()
    rows = cur.fetchall()
    con.close()
    
    print("Database conection: %d" % (int(round(time.time() * 1000))-millis))
    millis = int(round(time.time() * 1000))
    
    spectrums = []
    for row in rows:
        spectrums.append(row[4].split(","))
    
    print("Fetch data: %d" % (int(round(time.time() * 1000))-millis))
    millis = int(round(time.time() * 1000))
    
    wl = range(1100, 2450,2)
    
    #The plot stuff is extremely time consuming (x100 the operations of the database and data fetching)
    for spectrum in spectrums:
        plt.plot(wl, spectrum)
    
    print("Plot: %d" % (int(round(time.time() * 1000))-millis))
    millis = int(round(time.time() * 1000))
    
    plt.grid()
    plt.show()
        