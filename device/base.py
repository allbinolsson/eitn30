import time
import struct
from device import Device

class Base (Device):

    def __init__(self, radios, role = "T"):
        self.radio_number = 0   
        Device.__init__(self, radios, role)