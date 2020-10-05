#python.exe d:\jobs\rtrRf\sources\rtrMisc\motorAutoRecord\doIt.py
#file saved at: D:\jobs\rtrRf\sources\rtrMisc\motorAutoRecord\output
file_save_at = 'D:\\jobs\\rtrRf\\sources\\rtrMisc\\motorAutoRecord\\output\\'
import os
import threading
from pymavlink import mavutil
import time
from datetime import datetime
os.getcwd()



from pymavlink.dialects.v20 import ardupilotmega as mavlink2
VIANS_DATALINK_MODULE = 'tcp:192.168.0.210:20002'
master = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega")


throttle = 0 #using channel 5
voltage = 0
current = 0
FILE_OPENED = 0
print "USING CHANNEL 5"
print "File name please: "
filename = raw_input()
filename =  os.path.join(file_save_at, filename + '.txt')
#filename = file_save_at + filename + '.txt'
print filename
filee = open(filename, 'w')
FILE_OPENED = 1
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
UINT16_MAX = 65535
def sendRC(num):
	
	mss = mavlink2.MAVLink_rc_channels_override_message(
                    master.target_system,
                    master.target_component,
                    UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					UINT16_MAX,
					num,
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
		while True:
			time.sleep(0.1)
			abc = raw_input()
			if abc == 't':
				#loiterUnLim(5000)
				print 'yeeeeeeeeeeeeeeeeeeeeee'
				if FILE_OPENED:
					filee.close()
			elif abc[0:3] == 'rc,' and int(abc[3:7]):
				while True:
					time.sleep(0.1)
					rc = int(abc[3:7])
					sendRC(rc)
					print rc
					print 'Input kg, must include dau cham: '
					kg = raw_input()
					#print kg
					if '.' in kg:
						
						now = datetime.now()
						stttttrrr = str(rc)+', '+ kg+ ', '+ str(voltage)+', '+ str(current)
						print "WRITING: ", stttttrrr
						filee.write(str(now) + ' | ')
						filee.write(stttttrrr)
						filee.write('\n')
						print "WRTITEN"
						break
						
				

class sensorRead(threading.Thread):
	def __init__(self, threadID, name):	
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		global throttle
		global voltage
		global current
		while True:
			
			time.sleep(0.1)

_threadInput = threadInput(1, 'input')


_threadInput.start()


while True:
	msg = master.recv_match()
	if not msg:
		continue
		
	if msg.get_type() == 'BATTERY_STATUS':
		voltage = float(msg.voltages[0])/1000
		current = float(msg.current_battery)/100
	elif msg.get_type() == 'RC_CHANNELS':
		throttle = msg.chan5_raw
	time.sleep(0.1)
