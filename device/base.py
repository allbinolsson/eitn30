import time
import struct
from device import Device
from RF24 import RF24, RF24_PA_LOW

class Base (Device):

    def __init__(self, r1, role):
        self.radio_number = 0   
        Device.__init__(self, r1, role)