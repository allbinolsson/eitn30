import time
from longgeframe import Frame
from tun_device import TunDevice

class TunBase (TunDevice):
    def __init__(self, tunData, udpData):
        super().__init__(tunData, udpData)

    def findLargest(self, table):
        largest = 1
        for i in table:
            n = i.split(".")[3]
            largest = n if n > larger else largest
        return largest + 1