import time
import struct
from device import Device

class Mobile (Device):
    def __init__(self, r1, role):
        self.radio_number = 1
        Device.__init__(self, r1, role)