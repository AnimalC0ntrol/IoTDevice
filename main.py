import machine
import os
import pycom
from time import sleep
from startiot import Startiot
from common import *
from machine import Pin
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
from pir import Longpir
from led import Led


class AnimalAlert():
	def __init__(self):
		self.iot = Startiot()
		self.iot.connect(False)

		py = Pytrack()
		self.gps = L76GNSS(py, timeout = 30)
		self.acc = LIS2HH12(py)

		self.centerpir = Longpir("P11")
		self.led = Led("P10")
		
		pycom.heartbeat(False) # disable the blue blinking
		#self.sidepir = Shortpir("P11", "P10") 	

	def get_gps(self):
		(m_lat, m_lng) = self.gps.coordinates()
		return(m_lat, m_lng)


	def send(self, data):
		self.iot.send(data)


	def run(self):
		# main loop
		while True:
			val = self.centerpir.check_sensor()
			print(val)

			if val == 1:
				self.led.blink(1, 10)
				(m_lat, m_lng) = self.get_gps()
				data = "{},{},{}".format(val, m_lat, m_lng)
				print(data)
				self.send

			self.led.stop
			sleep(1)

if __name__=="__main__":
	aa = AnimalAlert()
	aa.run()