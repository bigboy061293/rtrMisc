import numpy as np
import matplotlib.pyplot as plt
import threading
set_point_fr = 2.00
k=10

# for controlling stuff via mavlink. would be in another bunch of code
# for reading stuff, there will be a block of code

#input of this class:
#1. set speed, almost constant
#2. raw fr read from sensor

#output of this:
#1. flowrate after filtering


fr_value_raw = np.zeros(2*k + 1)
pump_servo = 1100

#update
fr_sensor = 0.00 # read fr from sensor
fr_value_raw = np.roll(fr_value_raw,-1) # rolling in the deep
fr_value_raw[2*k] = fr_sensor 
#print kern
#print arr
#print out

kern=np.ones(2*k+1)/(2*k+1)
#arr=np.random.random((50)) + 2.5
out=np.convolve(fr_value_raw,kern, mode='same')
print out[2*k]
fr_filtered = out[2*k]
#fig, ax1 = plt.subplots()

#ax2 = ax1.twinx()

#print df
#plt.plot( arr, marker='',color='skyblue', linewidth=1)
#plt.plot( out, marker='', color='olive', linewidth=1)
#plt.plot( 2, 3, data=df, marker='', color='olive', linewidth=2, linestyle='dashed', label="toto")
#plt.legend()
#plt.show()
while True:
	if fr_filtered < (set_point_fr - 0.2):
		

		pump_servo+=1
		#output 
	elif fr_filtered > (set_point_fr + 0.2):
		pump_servo+=1
	if pump_servo < 1100:
		pump_servo = 1100
	elif pump_servo >1900:
		pump_servo = 1900
	print pump_servo
	# send messgae outPump
	pass