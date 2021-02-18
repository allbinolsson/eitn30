import socket
from tuntap import TunTap
class TunDevice:
    def __init__(self, tunData, udpData):
        self.tun = TunTap(nic_type="Tun", nic_name="longge")
        self.tun.config(ip=tunData[0], mask=tunData[1])
        
        self.UDP = udpData
        self.txSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rxSocket.bind((udpData[0], udpData[2]))
    
    def transmit(self):
        print("Transmitting!")
        while True:
            buf = self.tun.read()
            self.txSocket.sendto(buf, (self.UDP[1], self.UDP[2]))

    def receive(self):
        print("Receiving!")
        while True:
            rcvd, addr = self.rxSocket.recvfrom(1024)
            self.tun.write(rcvd)
            print("Received: {}\tFrom address: {}".format(rcvd, addr))