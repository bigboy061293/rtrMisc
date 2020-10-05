import socket
import time
import turtle

#import matplotlib.animation as animation
from matplotlib import style
import sys
import pyqtgraph as pg
#from PyQt4.QtWidgets import QApplication
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation
from datetime import datetime
import npyscreen
import curses
UDP_IP = '192.168.0.111'
UDP_PORT = 2992

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

########
#
# Init conrua
#
########

#screenW = 1000
#screenH = 600
#radarShownScale = 20
#radarHeightLimit = 2
#wn = turtle.Screen()
#wn.title('RtR radar visulization')
#wn.bgcolor('black')
#wn.setup(screenW,screenH)
#wn.tracer(0)

#wnGUI = turtle.Screen()
#wn.title('MF GUI')
#wn.bgcolor('black')
#wn.setup(screenW,screenH)
#wn.tracer(0)

#grid = turtle.Turtle()
#MR72objs = turtle.Turtle()


class radarObject:
	
	ID = 0
	IDx = 0
	latX = 0.0
	longY = 0.0
	shownOff = 0

	def __init__ (self,ID,latX,longY,shownOff):
		self.ID = ID
		
		self.latX = latX
		self.longY = longY
		self.shownOff = shownOff
		
		
	def parseMessgageToArrayMR72 (self,message):
		
		self.ID = message.data[0]
		self.longY = (message.data[1] * 32 + (message.data[2] >> 3)) * 0.2 - 500
		self.latX = ((message.data[2]&0X07) * 256 + message.data[3]) * 0.2 - 204.6
		self.shownOff = 0

arrayMR72 = []
arrayMR72marker = []
arrayMR72Turtle = []
for i in range(256):
	arrayMR72.append(radarObject(0,0,0,0))
#	arrayMR72Turtle.append(turtle.Turtle())
#	arrayMR72Turtle[i].speed(0)
#	arrayMR72Turtle[i].shape('circle')
#	arrayMR72Turtle[i].color('red')
#	arrayMR72Turtle[i].shapesize(stretch_wid = 0.5, stretch_len = 0.5)
#	arrayMR72Turtle[i].penup()
#	arrayMR72Turtle[i].goto(0,0)
#	arrayMR72Turtle[i].hideturtle()
		
tempID = []
tempLatX = []
tempLongY = []



#win=pg.GraphicsWindow()
#p1=win.addPlot()
#my_data=pg.ScatterPlotItem(tempLatX,tempLongY,symbol='o',size=30)
#p1.addItem(my_data)





def mainFx(stdscr):
	stdscr.addstr(15,15,"hl")
	stdscr.refresh()
	time.sleep(0.01)
	#time.sleep(0.01)
	#wn.update()
	#plt.pause(0.000001)
	data, addr = sock.recvfrom(32) # buffer size is 1024 bytes
	print "received message:", data
	abc = data.split(',')
	
	if data.find('---') == -1:
		
		tempID.append(int(abc[0]))
		tempLatX.append(float(abc[1]))
		tempLongY.append(float(abc[2]))
		
		
		#arrayMR72[tempID].shownOff = 1
		#arrayMR72[tempID].latX = tempLatX
		#arrayMR72[tempID].longY = tempLongY
		
	else:
		print(tempID)
		#pg.plot(tempLatX, tempLongY, pen=None, sy
	
		
		del tempID[:]
		del tempLatX[:]
		del tempLongY[:]
	
	
		#for i in range(256):
			#if arrayMR72[i].shownOff == 1:
				#process to display
				#arrayMR72[i].shownOff = 0
	now = datetime.now()
	currenTimeCreateFile = int(now.strftime("%H%M%S%f"))
	#print (currenTimeCreateFile)
	"""
	if currenTimeCreateFile - beforeTimeCreateFile > 1000:
	
		print(currenTimeCreateFile)
		sc.set_offsets(np.c_[x,y])
		fig.canvas.draw_idle()
		plt.pause(0.01)
	beforeTimeCreateFile = currenTimeCreateFile
	"""
	
curses.wrapper(mainFx)