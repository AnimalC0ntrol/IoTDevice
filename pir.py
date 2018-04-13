from machine import Pin
import time
import pycom
from common import *


class Longpir:
    def __init__(self, pinnumber):
        self.sensor = Pin(pinnumber, mode=Pin.IN, pull=Pin.PULL_DOWN)

    def check_sensor(self):
        value = self.sensor()
        if value == 1:
            print("Detected a moose")
    
        return value

class Shortpir:
    def __init__(self, pin1, pin2):
        self.pin1 = Pin(pin1, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.pin2 = Pin(pin1, mode=Pin.OUT, pull=Pin.Pull_DOWN)
        self.state = False

    def check_sensors(self):
        pass
