import socket
import ipaddress
from longgeframe import Frame, FrameReader
from tuntap import TunTap

class TunDevice:
    def __init__(self, tunData, udpData):
        self.ip = tunData[0]
        self.mask = tunData[1]
        self.tun = TunTap(nic_type="Tun", nic_name="longge")
        self.tun.config(ip=tunData[0], mask=tunData[1])
        
        self.UDP = udpData
        self.txSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rxSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rxSocket.bind((udpData[0], udpData[2]))

        self.fr = FrameReader()
        self.routingtable = []

    # Handshake helper function
    def assignIP(self, ip):
        newIp = ip
        if ip in self.routingtable:
            parts = ip.split('.')
            for i in range(2, 255): # 1 is base, 255 is broadcast (?)
                newIp = str(parts[0] + "." + parts[1] + "." + parts[2] + "." + str(i))
                if newIp not in self.routingtable:
                    break
        return newIp

    def handshake(self, fragment, data = None):
        if fragment == 0:
            request = str(ipaddress.IPv4Address(data))
            response = self.assignIP(request)
            if response not in self.routingtable: self.routingtable.append(response)  # this should be done after an ACK
            
            frame = Frame(1, fragment + 1, int(ipaddress.IPv4Address(response)))
            self.txSocket.sendto(frame.getFrame().encode(), (self.UDP[1], self.UDP[2]))
        elif fragment == 1:
            if data is not None: print(data)
            self.tun.config(ip=str(ipaddress.IPv4Address(data)), mask=self.tun.mask)
            print("ip updated:", self.tun.ip)
        # Room to add an ack part as well

    def transmit(self):
        print("Transmitting!")
        while True:
            buf = self.tun.read()
            if buf.hex()[:2] == "45":
                print("read:", buf.hex())
                self.txSocket.sendto(buf, (self.UDP[1], self.UDP[2]))

    # receive helper function
    # 45 for ip
    # 30 for longge
    def packetType(self, rcvd):
        return rcvd.hex()[:2]

    def receive(self):
        print("Receiving!")
        while True:
            rcvd, addr = self.rxSocket.recvfrom(1024)
            if self.packetType(rcvd) == "45":
                print("received:", rcvd.hex(), "with lenght:", len(rcvd))
                self.tun.write(rcvd)
            elif self.packetType(rcvd) == "30":
                if self.fr.plane(rcvd) == 1:
                    if self.fr.fragment(rcvd) == 0: print("Initiating handshake!")
                    self.handshake(self.fr.fragment(rcvd), self.fr.data(rcvd))
                
