def get_image(param):
    im=Image.open('/home/pi/signal_processing/flask/little_server/' + 'source.jpg')
    im=im.rotate(param[4])
    im = im.crop(box=param[:4])
    img_spectrum = im.load()
    return img_spectrum

def get_baseline(img_spectrum, param):
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
    black_line = [(rl[i]+gl[i]+bl[i])/3. for i in range(len(rl))]

def process_image():
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
        
        plt.plot(normalized,c='purple'); #plt.show()
        savefig('/home/pi/signal_processing/flask/little_server/' + 'static/spectrum.png', bbox_inches='tight')
        return 0
    except:
        print("Unable to save image")
        return 0