#!/usr/bin/python3
import serial
import cherrypy
import threading
import time
import datetime
import queue

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

blink=0

def serialread():  #Continuous loop to read serial
	global blink
	while True:
		line=ser.readline()
		serRead=line.decode('utf-8')

		if serRead == "b\r\n":					#Start of frame
			blink = blink + 1
			print(blink)


class Web(object):
	@cherrypy.expose
	def query(self,reset=0):
		global blink
		count = blink #Write an actual number if reset
		if reset == "1":
			blink=0
		return str(count)

sreadqueue		= queue.Queue()	#Queue for packets coming from the serial

serialreadThread = threading.Thread(target=serialread)
serialreadThread.start()

cherrypy.server.socket_host = "0.0.0.0"
cherrypy.quickstart(Web())
