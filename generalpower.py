#!/usr/bin/python3
import serial
import cherrypy
import threading
import time
import datetime
import queue

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

blink=0
lastquery=0


def serialread():  #Continuous loop to read serial
		global blink
		while True:
			line=ser.readline()
			serRead=line.decode('utf-8')

			if serRead == "b\r\n":                                  #Start of frame
				blink = blink + 1
				print(blink)

def failsafe(): #If no web reading in last 15 seconds, delete data
		while True:
			global lastquery
			global blink
			if time.time() - lastquery > 12:
				blink=0
				print("reset")
			time.sleep(0.1) 

class Web(object):
		@cherrypy.expose
		def query(self,reset=0):
			global blink
			global lastquery
			count = blink #Write an actual number if reset
			if reset == "1":
				lastquery = time.time()
				blink=0
			return str(count)

serialreadThread = threading.Thread(target=serialread)
serialreadThread.start()

failsafeThread = threading.Thread(target=failsafe)
failsafeThread.start()

cherrypy.server.socket_host = "0.0.0.0"
cherrypy.server.socket_port = 8081
cherrypy.quickstart(Web())
