import machine
import math
import network
import os
import pycom
import socket
import utime
from time import sleep
from startiot import Startiot
from common import *
from machine import Pin
from machine import RTC
from machine import SD
from machine import Timer
from L76GNSS import L76GNSS
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack

iot = Startiot()
iot.connect(False)

py = Pytrack()
gps = L76GNSS(py, timeout = 30)
acc = LIS2HH12(py)
pir = Pin('P11',mode=Pin.IN,pull=Pin.PULL_DOWN)

pycom.heartbeat(False) # disable the blue blinking
pycom.rgbled(0x000000) #LED off

state = False
# main loop
while True:
  val = pir()
  print('Value:', val)

  if state == False:
    if val == 1:
      print('----------------------------------')

      state = True
      pycom.rgbled(colors["red"])
      (m_lat, m_lng) = gps.coordinates()
      #print('Coordinates:', "{},{}".format(m_lat, m_lng))

      data = "{},{},{}".format(val, m_lat, m_lng)
      #data = "MOTION,1"
      iot.send(data)
      print(data)
      sleep(10)
  else:
    if val == 0:
      pycom.rgbled(colors["black"])
      state = False
    
  sleep(1)

  


