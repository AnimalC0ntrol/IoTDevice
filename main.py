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


class AnimalAlert():
	def __init__(self):
		self.iot = Startiot()
		self.iot.connect(False)

		py = Pytrack()
		self.gps = L76GNSS(py, timeout = 30)
		self.acc = LIS2HH12(py)
		#pir = Pin('P11',mode=Pin.IN,pull=Pin.PULL_DOWN)
		self.longpir = Longpir("P11")
		pycom.heartbeat(False) # disable the blue blinking

	def run(self):
		# main loop
		while True:
			val = self.longpir.check_sensor()
			print(val)

			if val == 1:
				(m_lat, m_lng) = self.gps.coordinates()
				data = "{},{},{}".format(val, m_lat, m_lng)
				print(data)
				self.iot.send(data)
				sleep(10)
			sleep(1)

if __name__=="__main__":
	aa = AnimalAlert()
	aa.run()