import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.signal as sps
import sqlite3 as sqlite
import time

def better_local(derivative,real_value,wl,CAL_V, kind):
    """
    Function that get a spectrum (real_value), his derivative function (derivative), CAL_V and the kind of data 
    Returns a dictionary of the x and y values of the minima or maxima in the spectrum
    """
     
    indexes = []
    final = []
    
    #Get all possible points (thanks to the derivative function)
    for i in range(len(derivative)):
        if(kind == "minima"):
            if(derivative[i] <= CAL_V[0] and derivative[i] >= -CAL_V[0] and len(derivative)-i >10):
                if(i==0 or i== len(derivative)-1):
                    final.append(real_value[i])
                    indexes.append(1100+ i*2)
                elif(derivative[i] > derivative[i-1]+CAL_V[1] and derivative[i+1] > derivative[i]+CAL_V[1]):
                    final.append(real_value[i])
                    indexes.append(1100+ i*2)
        elif(kind == "maxima"):
            if(derivative[i] <= CAL_V[0]*2 and derivative[i] >= -CAL_V[0]*2 and len(derivative)-i >10):
                if(i==0 or i== len(derivative)-1):
                    final.append(real_value[i])
                    indexes.append(1100+ i*2)
                elif(derivative[i] < derivative[i-1]-CAL_V[1]*2 and derivative[i+1] < derivative[i]-CAL_V[1]*2):
                    final.append(real_value[i])
                    indexes.append(1100+ i*2)
         
    dictionary = {"x": indexes, "y":final}
    
    indexes = []
    final = []
    total_list = []
    total_avg = []
    temp_list = []
    
    #Make the average of the minima/maxima points that are really near
    for i in range(len(dictionary['x'])-1):
        if(dictionary['x'][i+1]-dictionary['x'][i] < CAL_V[2]):
            if(temp_list == []):
                temp_list.append(i)
            temp_list.append(i+1)
        else:
            if(temp_list != []):
                avg = 0
                for j in range(len(temp_list)):
                    avg = avg + dictionary['x'][temp_list[j]]
                avg = avg / len(temp_list)
                avg = avg//2
                avg = int(avg *2)
                total_avg.append(avg)
                for j in range(len(temp_list)):
                    total_list.append(temp_list[j])
                temp_list = []
                
    if(temp_list != []):
        avg = 0
        for j in range(len(temp_list)):
            avg = avg + dictionary['x'][temp_list[j]]
        avg = avg / len(temp_list)
        avg = avg//2
        avg = int(avg *2)
        total_avg.append(avg)
        for j in range(len(temp_list)):
            total_list.append(temp_list[j])
        temp_list = []
        
    #Delete the points that are near to each others that we have found above
    for i in range(len(total_list)-1, -1,-1):
        #print("Deleting %d" % dictionary['x'][total_list[i]])
        del dictionary['x'][total_list[i]]
        del dictionary['y'][total_list[i]]
    
    almost_x = []
    almost_y = []
    #In the dictionary to_send all the x values of the minima points
    for i in range(len(dictionary['x'])):
        almost_x.append(dictionary['x'][i])
    for i in range(len(total_avg)):
        almost_x.append(total_avg[i])
    
    #Find the corresponding y value for the informations on the x axis of the local minima
    for i in almost_x:
        almost_y.append(real_value[np.where(wl==i)[0][0]])
    
    #Sort the minima
    indexes_to_sort = np.argsort(almost_x)
    x = [almost_x[i] for i in indexes_to_sort]
    y = [almost_y[i] for i in indexes_to_sort]
    dictionary = {'x': x, 'y': y}
    
    return dictionary

def regression_line(points):
    '''
    Function that takes the points of the minima and outputs the regression line with less error
    The possible regression lines are:
        poly 1
        poly 2
        poly 3
        poly 4
    '''
    fit = np.polyfit(points['x'], points['y'], deg=2) 
    fit_fn = np.poly1d(fit)
    return fit_fn
    
    

if __name__ == '__main__':

    # Set the working directory
    prjdir = '' #Current directory

    # Read the data from a csv file. Columns separated by \t.
    # The first line of the file contains the scanned wavelengths
    tmpdata = np.loadtxt(os.path.join(prjdir, 'marzipan.csv'), delimiter='\t')
    wl = tmpdata[0] #Wavelenght
    spectrum = tmpdata[1:]

    # Get dataset dimension
    n, p = spectrum.shape

    final_spectrum = []
    con = sqlite.connect('samples.db')
    cur = con.cursor()
    # Do the same things for all the spectrum
    for h in range(n):
        almost_good = spectrum[h, :]
        good_f = sps.savgol_filter(almost_good.tolist(), 51, 3)
        
        h = max(good_f)-min(good_f)
        l = max(wl)-min(wl)
        
        #Calibration values
        CAL_V = [0.0008 / 1.5 * h, 0.0001 / 1.5 * h, 20 / 1300 * l]
        
        #Get derivative function
        derivative = np.diff(good_f)
        
        #print ("%d %d" % (len(wl[:-1]), len(derivative)))
        
        #get the x data for the local minima
        minima = better_local(derivative,good_f, wl,CAL_V, "minima")
        
        fit_fn = regression_line(minima)
        
        #print ("Error: %f" % error)
        
        #Calculate the normalized spectrum
        #min([(good_f[i] - fit_fn(i*2 + 1100)) for i in range(675) ])
        fit_fn_list =  fit_fn(range(1100, 2450, 2))
        normalized = good_f - fit_fn_list
        min_normalized = min(good_f - fit_fn_list)
        normalized = np.array([normalized[i] - min_normalized for i in range(675)])
        #plt.plot(wl, fit_fn(wl),'-', color="purple") #Show fitting line
        derivative = np.diff(normalized)
        maxima = better_local(derivative,normalized, wl,CAL_V, "maxima")
        #Find the corresponding y value for the informations on the x axis of the local minima
        
        final_spectrum.append(normalized)
        db_string = ""
        for i in normalized:
            db_string = ("%s,%s" % (db_string,str(round(i,4))))
        
        db_string = db_string[1:]
        
        cur.execute("INSERT INTO Samples (grower,field,timestamp,spectrum,gps) VALUES (1,2,%d,\"%s\",0)" % (int(time.time()),db_string))
con.commit()
data = cur.fetchone()
print(data)
con.close()