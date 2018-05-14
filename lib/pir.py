from machine import Pin
import time
import pycom

class Pir():
    def __init__(self, pinnumber):
        self.sensor = Pin(pinnumber, mode=Pin.IN, pull=Pin.PULL_DOWN)

    def check_sensor(self):
        value = self.sensor()
        if value == 1:
            print("Detected a moose")
    
        return value
