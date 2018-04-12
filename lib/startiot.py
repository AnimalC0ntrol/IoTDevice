from network import LoRa
import socket
import time
import binascii
import pycom
import machine

class Startiot:

    def __init__(self):
        self.dev_eui = binascii.unhexlify("ffffffff00001366")
        self.app_eui = binascii.unhexlify("8000000000000006")
        self.app_key = binascii.unhexlify("b2d5d65e548a5e68cc6e1d733cc0431e")

        self.lora = LoRa(mode=LoRa.LORAWAN)
    def connect(self, blocking):
        self.lora.join(activation=LoRa.OTAA, auth=(self.dev_eui, self.app_eui, self.app_key), timeout=0)

        while not self.lora.has_joined():
            pass

        self.s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        self.s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

        # make the socket non-blocking
        self.s.setblocking(blocking)

    def send(self, data):
        self.s.send(data)

    def recv(self, length):
        return self.s.recv(length)
