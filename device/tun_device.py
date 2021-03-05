import socket
import ipaddress
import math
import time
# import queue
from longgeframe import Frame, FrameReader
from tuntap import TunTap
from RF24 import RF24, RF24_PA_LOW, RF24_2MBPS

class TunDevice:
    def __init__(self, tunData, radios):
        # init tun
        self.ip = tunData[0]
        self.mask = tunData[1]
        self.tun = TunTap(nic_type="Tun", nic_name="longge")
        self.tun.config(ip=self.ip, mask=self.mask)

        # init nrf24
        self.radios = radios
        self.address = [b'1Node', b'2Node']
        self.radioNumber = 0 if self.tun.ip == "192.168.2.1" else 1
        for r in self.radios:
            if not r.begin():
                raise RuntimeError("Hardware Error")
            r.setPALevel(RF24_PA_LOW)
            r.openWritingPipe(self.address[self.radioNumber])
            r.openReadingPipe(1, self.address[not self.radioNumber])
            r.payloadSize = 32 
            r.setAutoAck(False) # config chip --------------
            r.disableCRC() 
            r.setDataRate(RF24_2MBPS)        
        
        # misc
        self.fr = FrameReader()
        self.routingtable = []
        self.payloads = {}
        # self.sendQ = queue.Queue()
        # self.receiveQ = queue.Queue()

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

    def packetType(self, rcvd):
        return rcvd.hex()[:2]

    def handshake(self, fragment, data):
        if fragment == 0:
            request = str(ipaddress.IPv4Address(data))
            response = self.assignIP(request)
            if response not in self.routingtable: self.routingtable.append(response)  # this should be done after an ACK
            
            frame = Frame(1, 1, fragment + 1, 0, 0, format(int(ipaddress.IPv4Address(response)), "032b"))
            buf = self.fr.bits2bytes(frame.compile())
            self.radios[0].write(buf)
        elif fragment == 1:
            if data is not None: print(data)
            self.tun.config(ip=str(ipaddress.IPv4Address(data)), mask=self.tun.mask)
            print("ip updated:", self.tun.ip)
        # Room to add an ack part as well

    def dividePayload (self, bits):
        return [bits[i:i+Frame.DATA_LENGTH] for i in range(0, len(bits), Frame.DATA_LENGTH)]

    def sendBits(self, bits):
        tx = self.radios[0]
        
        payloads = self.dividePayload(bits)
        fragments = ""
        for i, b in enumerate(payloads):
            final = 1 if i == len(payloads) - 1 else 0
            frame = Frame(0,
                    final, # final fragment flag
                    i, # fragment number
                    int(ipaddress.IPv4Address(self.ip)),
                    0, # don't know which device I'm on
                    b
                )
            val = frame.compile()
            d = self.fr.data(val)
            fragments += d

            res = tx.write(self.fr.bits2bytes(frame.compile()))
            if not res:
                print("Transmission failed")
        # print("All fragments:", self.fr.bits2bytes(fragments).hex())

    def transmit(self):
        print("Transmitting!")
        tx = self.radios[0]
        tx.stopListening()

        while True:
            buf = self.tun.read()
            if buf.hex()[:2] != "60":   # "60" is some kind of OS dump
                bits = self.fr.bytes2bits(buf)
                self.sendBits(bits)


    def handlePayloads(self):        
        bits = ""
        for k in self.payloads.keys():
            bits += self.payloads[k]
        # print("Accumulated data:", self.fr.bits2bytes(bits).hex())
        self.tun.write(self.fr.bits2bytes(bits))
        # print("Tun got:", self.fr.bits2bytes(bits).hex())
        

    def receive(self):
        print("Receiving!")
        rx = self.radios[1]
        rx.startListening()

        while True:
            hasPayload, pipeNo = rx.available_pipe()
            if hasPayload:
                rcvd = rx.read(rx.payloadSize)
                bits = self.fr.bytes2bits(rcvd)
                if self.fr.plane(bits) == 0:
                    f = self.fr.fragment(bits)
                    self.payloads[f] = self.fr.data(bits)
                    if self.fr.final(bits): 
                        self.handlePayloads()
                elif self.fr.plane(bits) == 1:
                    self.handshake(self.fr.fragment(bits), int(self.fr.data(bits), 2))