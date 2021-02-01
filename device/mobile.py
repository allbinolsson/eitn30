import time
import struct
from device import Device

class Mobile (Device):
    def __init__(self, radios, role = "R"):
        self.radio_number = 1
        Device.__init__(self, radios, role)