import time
from longgeframe import Frame
from tun_device import TunDevice

class TunBase (TunDevice):
    def __init__(self, tunData, udpData):
        super().__init__(tunData, udpData)