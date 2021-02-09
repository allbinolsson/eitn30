import time
import struct
from device import Device

class Mobile (Device):
    def __init__(self, radios, role = "M"):
        Device.__init__(self, radios, role)