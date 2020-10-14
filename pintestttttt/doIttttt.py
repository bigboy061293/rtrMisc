#python.exe D:\jobs\rtrRf\sources\rtrMisc\pintestttttt\doIttttt.py
#file saved at: D:\jobs\rtrRf\sources\rtrMisc\pintestttttt\output
#Sua duong dan file save at

file_save_at = 'D:\\jobs\\rtrRf\\sources\\rtrMisc\\pintestttttt\\output\\'



import os
import subprocess, signal
import threading
from pymavlink import mavutil
import time
from datetime import datetime
import numpy as np
import win32pdh, string, win32api
os.getcwd()

from pymavlink.dialects.v20 import ardupilotmega as mavlink
VIANS_DATALINK_MODULE = 'tcp:192.168.0.210:20002'
master = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega", source_system=255, source_component=29)


throttle = 1100 #using channel 5
throttleMotor = 1100
k = 20
voltage = 0
voltageMin = 0
current = 0
FILE_OPENED = 0
PIN_MAX_POWER = 20400
PIN_MIN_POWER = 0
#check this
smith = 3
powerSet = 0
powerSens = 0
powerRaw = np.zeros(2*k+1)
powerConv = 0
FILE_OPENED = 0
returnF = False
print "USING CHANNEL 1 2 3 4"
if FILE_OPENED:
	print "File name please: "
	filename = raw_input()
	filename =  os.path.join(file_save_at, filename + str(datetime.now()) + '.txt')
	#filename = file_save_at + filename + '.txt'
	print filename
	filee = open(filename, 'w')

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
master.mav.command_long_send(
    master.target_system, master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
    147, 100, 0, 0, 0, 0, 0)
 
UINT16_MAX = 65535
def procids():
    #each instance is a process, you can have multiple processes w/same name
    junk, instances = win32pdh.EnumObjectItems(None,None,'process', win32pdh.PERF_DETAIL_WIZARD)
    proc_ids=[]
    proc_dict={}
    for instance in instances:
        if instance in proc_dict:
            proc_dict[instance] = proc_dict[instance] + 1
        else:
            proc_dict[instance]=0
    for instance, max_instances in proc_dict.items():
        for inum in xrange(max_instances+1):
            hq = win32pdh.OpenQuery() # initializes the query handle 
            path = win32pdh.MakeCounterPath( (None,'process',instance, None, inum,'ID Process') )
            counter_handle=win32pdh.AddCounter(hq, path) 
            win32pdh.CollectQueryData(hq) #collects data for the counter 
            type, val = win32pdh.GetFormattedCounterValue(counter_handle, win32pdh.PDH_FMT_LONG)
            proc_ids.append((instance,str(val)))
            win32pdh.CloseQuery(hq) 

    proc_ids.sort()
    return proc_ids

def sendRC(throttleMotor):
	mss = mavlink.MAVLink_rc_channels_override_message(
                    master.target_system,
                    master.target_component,
                    throttleMotor,
					throttleMotor,
					throttleMotor,
					throttleMotor,
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
				except:
					powerSet = 0
					throttleMotor = 1100
				pass
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
			time.sleep(0.01)
			
			if voltage >= voltageMin:
				powerRaw = np.roll(powerRaw,-1) # rolling in the deep
				powerRaw[2*k] = powerSens 

				powerConv = np.average(powerRaw)

				print 'Set Power: ', powerSet, ', ', ' Current Power: ', powerConv,', ', 'Current PWM: ', throttleMotor
				if powerConv < (powerSet - smith):
					throttleMotor+=5
				#output 
				elif powerConv > (powerSet + smith):
					throttleMotor-=5
				if throttleMotor < 1100:
					throttleMotor = 1100
				elif throttleMotor >1940:
					throttleMotor = 1940
			else: 
				throttleMotor=1100
			sendRC(throttleMotor)	
_threadInput = threadInput(1, 'input')
_threadInput.start()
_outRC = outRC(2,'outrc')
_outRC.start()

while True and not returnF:
	
	time.sleep(0.1)
	msg = master.recv_match()
	if not msg:
		continue
	
	
	if msg.get_type() == 'BATTERY_STATUS':
		voltage = float(msg.voltages[0])/1000
		current = float(msg.current_battery)/100
		powerSens = int(voltage * current)
		#print powerSens
	elif msg.get_type() == 'RC_CHANNELS':
		#throttle = msg.chan5_raw
		pass
	
	
