#python.exe D:\jobs\rtrRf\sources\rtrMisc\pintestttttt\dodododo.py
#file saved at: D:\jobs\rtrRf\sources\rtrMisc\pintestttttt\output
#Sua duong dan file save at
import os
import subprocess, signal
import threading
from pymavlink import mavutil
import time
from datetime import datetime
import numpy as np
from tkinter import Tk, Label, Spinbox
 
os.getcwd()

from pymavlink.dialects.v20 import ardupilotmega as mavlink2
file_save_at = 'D:\\jobs\\rtrRf\\sources\\rtrMisc\\pintestttttt\\output\\'
VIANS_DATALINK_MODULE = 'tcp:192.168.0.210:20002'
master = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega", source_system=255, source_component=29)

timeBootMs = 0
throttle = 1100 #using channel 5
throttleMotor = 1100
throttleMotorStep = 5
k = 5
energyConsumption = 0
voltage = 36
voltageMin = 0
current = 0
FILE_OPENED = 0
PIN_MAX_POWER = 10000
PIN_MIN_POWER = 0
#check this
smith = 50
powerSet = 0
powerSens = 0
powerRaw = np.zeros(2*k+1)
powerConv = 0
FILE_OPENED = 1
returnF = False
print "USING CHANNEL 1 2 3 4"
if FILE_OPENED:

	print "File name please: "
	filename = raw_input()
	now = datetime.now()
	filename =  os.path.join(file_save_at, filename +'_' + now.strftime("%m%d%H%M%S") + '.txt')
	#filename = file_save_at + filename + '.txt'
	print 'okbd, filename = ', filename
	filee = open(filename, 'w')
	
print "Min voltage please: "
try:
	voltageMin = int(raw_input())
	print 'okbd, voltageMin = ', voltageMin
except:
	print 'Ngu, thoat lam lai'

print "Set power please: "
try:
	powerSet = int(raw_input())
	print 'okbd, set power = ', powerSet
except:
	print 'Ngu, thoat lam lai'
	
def connectToSim(master):
    msg = None
    while not msg:
        master.mav.ping_send(
            time.time(), # Unix time
            0, # Ping number
            0, # Request ping of all systems
            0 # Request ping of all components
        )
        msg = master.recv_match()
		
        time.sleep(0.5)

connectToSim(master)
time.sleep(1)
"""
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
    147, 100, 0, 0, 0, 0, 0)
"""
UINT16_MAX = 65535

def sendRC(throttleMotor):
	mss = mavlink2.MAVLink_rc_channels_override_message(
                    master.target_system,
                    master.target_component,
                    throttleMotor,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					throttleMotor,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX	
                    )
            # sending terrain end  ....................
	master.mav.send(mss)

class threadInput(threading.Thread):
    def __init__(self, threadID, name):	
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
		global throttle
		global powerSet
		global throttleMotor
		global returnF
		while True:
			time.sleep(0.05)
			
			abc = raw_input()
			inAbc = abc.split()
			if abc == 't':
				#loiterUnLim(5000)
				print 'yeeeeeeeeeeeeeeeeeeeeee'
				if FILE_OPENED:
					filee.close()
				#os.kill(os.getpid(), signal.SIGKILL)
				throttleMotor = 1100
				returnF = True
				sendRC(throttleMotor)
				
				time.sleep(0.5)
				
				return
				
			elif inAbc[0] == 'p':
				try:
					powerSet = int(inAbc[1])
					print 'Okbd, power = ',powerSet
				except:
					powerSet = 0
					throttleMotor = 1100
					
				continue
			elif inAbc[0] == 'g':
				try:
					#powerSet = int(inAbc[1])
					throttleMotor = int(inAbc[1])
					print 'Okbd, ga = ',powerSet
				except:
					
					throttleMotor = 1100
					
				continue
			elif abc == 'h':
				print ('Set Power: ', powerSet, 
						'voltage: ', voltage,
						'current: ', current,
						'energy: ', energyConsumption,
						'Power: ', round(powerConv,2),
						'PWM: ', throttleMotor)
				continue
			elif abc == 's':
				throttleMotor = 1100
				
				
class outRC(threading.Thread):
    def __init__(self, threadID, name):	
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
		
    def run(self):
		global throttleMotor
		global powerConv
		global powerRaw
		
		while True and not returnF:
			time.sleep(0.1)
			print ('Set Power: ', powerSet, 
						'voltage: ', voltage,
						'current: ', current,
						'energy: ', energyConsumption,
						'Power: ', round(powerConv,2),
						'PWM: ', throttleMotor)
			if voltage >= voltageMin:
				powerRaw = np.roll(powerRaw,-1) # rolling in the deep
				powerRaw[2*k] = powerSens 

				powerConv = np.average(powerRaw)
				sendRC(throttleMotor)
				
			#	if powerConv < (powerSet - smith):
			#		throttleMotor+=throttleMotorStep
				#output 
			#	elif powerConv > (powerSet + smith):
			#		throttleMotor-=throttleMotorStep
			#	if throttleMotor < 1100:
			#		throttleMotor = 1100
			#	elif throttleMotor >1940:
			#		throttleMotor = 1940
			#else: 
			#	throttleMotor=1100
			else:
				sendRC(1100)
				time.sleep(0.5)
				print 'Done, < volt min'
				return
			#print powerConv
			if FILE_OPENED:
				filee.write(str(datetime.now()) +',' +str(timeBootMs) + ',' + str(voltage)+ ',' + str(current)+ ',' + str(energyConsumption) + ',' + str(throttleMotor)+ ',' + str(powerSens) + '\n')
class readIp(threading.Thread):
    def __init__(self, threadID, name):	
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
		
    def run(self):
		global voltage
		global current
		global energyConsumption
		global powerSens
		while True and not returnF:
			msg = master.recv_match()
			if not msg:
				continue
				
					
			if msg.get_type() == 'BATTERY_STATUS':
				voltage = float(msg.voltages[0])/1000
				current = float(msg.current_battery)/100
				energyConsumption = msg.energy_consumed
				powerSens = int(voltage * current)
				#print powerSens
			elif msg.get_type() == 'RC_CHANNELS':
				timeBootMs = msg.time_boot_ms
				pass
def conNew(i, a, b):
	if i <= a:
		return a
	if i >= b:
		return b
	return i
def callback():
	global throttleMotor
	
	throttleMotor = conNew(int(spin.get()),1100,1900)
	
   # print("value:", spin.get())
	
			
		
_threadInput = threadInput(1, 'input')
_threadInput.start()
_outRC = outRC(2,'outrc')
_outRC.start()
_readIp = readIp(3,'form')
_readIp.start()


time.sleep(0.1)

#while True:
	#time.sleep(0.01)
	


window = Tk()
window.title("hihi tittle thoi ma ^^")
window.geometry('600x200')


time.sleep(0.5)
lbl = Label(window, text="PWM Out:           ")
lbl.grid(column=0, row=0)


spin = Spinbox(window, from_=1000, to=2000, width=10, command=callback)

spin.grid(column=1,row=0)


window.mainloop()
	

