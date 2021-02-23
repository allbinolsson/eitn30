import time
import ipaddress
from longgeframe import Frame, FrameReader
from tun_device import TunDevice

class TunMobile (TunDevice):
    def __init__(self, tunData, udpData):
        super().__init__(tunData, udpData)