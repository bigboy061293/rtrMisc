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
from pymavlink.dialects.v20 import ardupilotmega as mavlink
VIANS_DATALINK_MODULE = 'tcp:192.168.0.210:20002'
master = mavutil.mavlink_connection(VIANS_DATALINK_MODULE, dialect = "ardupilotmega", source_system=255, source_component=29)


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


while True:
	#sendRC(throttle)
	msg = master.recv_match()
	if not msg:
		continue
	#print msg
	
	if msg.get_type() == 'BATTERY_STATUS':
		voltage = float(msg.voltages[0])
		current = float(msg.current_battery)
		print voltage
		print current
		#print msg
	elif msg.get_type() == 'RC_CHANNELS':
		#throttle = msg.chan5_raw
		#print msg.chan5_raw
		pass
	
	
