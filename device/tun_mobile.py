import time
import ipaddress
from longgeframe import Frame, FrameReader
from tun_device import TunDevice

class TunMobile (TunDevice):
    def __init__(self, tunData, radios):
        super().__init__(tunData, radios)