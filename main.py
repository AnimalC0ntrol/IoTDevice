import machine
import os
import pycom
import utime
import _thread
import VEML6070
from time import sleep
from startiot import Startiot
from machine import Pin, I2C, RTC
from pir import *
from led import Led
from common import *
from pysense import Pysense


#from L76GNSS import L76GNSS
#from pytrack import Pytrack

class AnimalAlert():
	def __init__(self):
		self.iot = Startiot()
		self.iot.connect(False)
		self.py = Pysense()
		"""
		self.gps = L76GNSS(py, timeout = 30)
		(self.lat, self.lng) = self.gps.coordinates()
		self.counter = 0
		"""
		self.state = STATE_IDLE

		self.rightpir = Pir("P11")
		self.centerpir = Pir("P2") 
		self.leftpir = Pir("P9")
		self.led = Led("P10")
		self.i2c = I2C(1, I2C.MASTER, baudrate=100000, pins = ("P4", "P8"))
		self.uv_sensor = VEML6070.VEML6070_UV(self.i2c)
		self.baseline = []
		pycom.heartbeat(False) # disable the blue blinking
	"""
	def get_gps(self):		
		if (self.lat, self.lng) == (None, None):
			(self.lat, self.lng) = self.gps.coordinates()
		else: 
			if self.counter < GPS_NUMCOPIES:
				(self.lat, self.lng) = (self.lat, self.lng)
				self.counter += 1
			else: 
				self.counter = 1
				(self.lat, self.lng) = self.gps.coordinates()

		return(self.lat, self.lng)
	"""
	def uv_baseline(self, uv):
		if len(self.baseline) == BASELINE_MAX:
			self.baseline.pop(0)
			self.baseline.append(uv)
		else:
			self.baseline.append(uv)
		
		average = sum(self.baseline) / len(self.baseline)
		return average

	def notify(self, left, center, right):
		data = "{},{},{}".format(left, center, right)
		if center == 1: 
			self.state = STATE_WARNING
			self.iot.send(data)
			print("sent to startIoT")
			self.led.blink(LED_DELAY, LED_DURATION)

		elif left == 1 or right == 1:
			self.state = STATE_ALERT
			self.iot.send(data)
			print("sent to startIoT")
			self.led.blink(LED_DELAY, LED_DURATION)

		#(lat, lng) = self.get_gps()
		#data = "{},{},{},{},{},{}".format(left, center, right, lat, lng, uv)

	def run(self):
		# main loop
		while True:
			centerval = self.centerpir.check_sensor()
			rightval = self.rightpir.check_sensor()
			lefval = self.leftpir.check_sensor()
			uv = self.uv_sensor.read()
	
			average = self.uv_baseline(uv)
			print(lefval, centerval, rightval, uv, average)

			if centerval == 1 or lefval == 1 or rightval == 1:
				if uv > average + BASELINE_DIFF:
					pass
				else: 
					self.notify(lefval, centerval, rightval)
					self.state = STATE_IDLE

			self.led.stop
			sleep(SLEEPTIME_MAIN)

if __name__=="__main__":
	aa = AnimalAlert()
	aa.run()