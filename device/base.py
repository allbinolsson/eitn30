import time
import struct
from device import Device

class Base (Device):

    def __init__(self, radios, role = "B"): 
        Device.__init__(self, radios, role)