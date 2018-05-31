# Simple driver for the VEML6070 uv light sensor
from machine import I2C
class VEML6070_UV:
    def __init__(self, i2c, addr=0x38):
        self.i2c = i2c
        self.addr = addr
        self.value = 0
        i2c.writeto(self.addr, bytes([0x02])) # start continuos 1 Lux readings every 120ms

    def read(self):
        data = self.i2c.readfrom(self.addr, 2)
        self.value = (((data[0] << 8) | data[1]))
        return self.value