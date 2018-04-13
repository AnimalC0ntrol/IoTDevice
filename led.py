from machine import Pin
from time import sleep
import time
import pycom

class Led():
    def __init__(self, pinnumber):
        self.light = Pin(pinnumber, mode=Pin.OUT, value=1)

    def blink(self, delay, blinkingtime):
        numtimes = blinkingtime / delay
        for i in range(0, numtimes):
            self.light(1)
            sleep(delay)
            self.light(0)
            sleep(delay)

    def stop(self):
        self.light(0)