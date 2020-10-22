#python.exe D:\jobs\rtrRf\sources\rtrMisc\pintestttttt\doIttttt.py
#file saved at: D:\jobs\rtrRf\sources\rtrMisc\pintestttttt\output
#Sua duong dan file save at
import os
import subprocess, signal
import threading
from pymavlink import mavutil
import time
from datetime import datetime
import numpy as np
import win32pdh, string, win32api
os.getcwd()

from pymavlink.dialects.v20 import ardupilotmega as mavlink2
file_save_at = 'D:\\jobs\\rtrRf\\sources\\rtrMisc\\pintestttttt\\output\\'
VIANS_DATALINK_MODULE = 'tcp:192.168.0.210:20002'
master = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega")

timeBootMs = 0
throttle = 1100 #using channel 5
throttleMotor = 1100
throttleMotorStep = 2
k = 5
energyConsumption = 0
voltage = 0
voltageMin = 0
current = 0
FILE_OPENED = 0
PIN_MAX_POWER = 10000
PIN_MIN_POWER = 0
#check this
smith = 20
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
time.sleep(0.5)



master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
    65, 1000, 0, 0, 0, 0, 2)
time.sleep(0.5)
"""
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
    147, 10000, 0, 0, 0, 0, 2)
time.sleep(0.5)
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
					throttleMotor,
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
			time.sleep(0.2)
			
			if voltage >= voltageMin:
				

				
				if powerConv < (powerSet - smith):
					throttleMotor+=throttleMotorStep
				#output 
				elif powerConv > (powerSet + smith):
					throttleMotor-=throttleMotorStep
				if throttleMotor < 1100:
					throttleMotor = 1100
				elif throttleMotor >1940:
					throttleMotor = 1940
			else: 
				throttleMotor=1100
			sendRC(throttleMotor)
			if FILE_OPENED:
				#date time, time boot ms, voltage, current, power set, throttle, power sens
				filee.write(str(datetime.now()) +',' +str(timeBootMs) + ',' + str(voltage)+ ',' + str(current)+ ',' + str(powerSet) + ',' + str(throttleMotor)+ ',' + str(powerSens) + '\n')
_threadInput = threadInput(1, 'input')
_threadInput.start()
_outRC = outRC(2,'outrc')
_outRC.start()

while True and not returnF:
	
	time.sleep(0.01)
	msg = master.recv_match()
	if not msg:
		continue
	
	#print msg
	if msg.get_type() == 'BATTERY_STATUS':
		voltage = float(msg.voltages[0])/1000
		current = float(msg.current_battery)/100
		energyConsumption = msg.energy_consumed
		powerSens = int(voltage * current)
		
		powerRaw = np.roll(powerRaw,-1) # rolling in the deep
		powerRaw[2*k] = powerSens 

		powerConv = np.average(powerRaw)
		#print powerSens
	elif msg.get_type() == 'RC_CHANNELS':
		timeBootMs = msg.time_boot_ms
		pass
