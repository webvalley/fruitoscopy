import numpy as np
import cv2
import time
import matplotlib.pyplot as plt

img = cv2.imread('vajolet_1_1.jpg')
img_spectrum = img[1000:1200,1000:2200]
#cv2.imshow("img",img_spectrum)
#cv2.waitKey()

rl=np.zeros(1200);gl=np.zeros(1200);bl=np.zeros(1200);

for col in range(img_spectrum.shape[1]):
	count=[0.,0.,0.]
	for row in range(img_spectrum.shape[0]):
		b,g,r = img_spectrum[row,col]
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

plt.plot(rl,c='r');plt.plot(gl,c='g');plt.plot(bl,c='b');plt.plot((rl+gl+bl)/3.,c='black');plt.xlim([800,2500]);plt.show()