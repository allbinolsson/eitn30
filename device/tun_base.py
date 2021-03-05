import time
from tun_device import TunDevice

class TunBase (TunDevice):
    def __init__(self, tunData, radios):
        super().__init__(tunData, radios)