import threading
import time
import struct
from device import Device

class Duplex:
    def printInfo(self, interval):
        timer = time.monotonic()
        while True:
            newTime = time.monotonic()
            if newTime - timer >= interval:   # ugly busy wait
                timer = newTime
                self.totalTime += 1
                print(
                    "Seconds passed: {}\t"
                    "Sent: {}\t"
                    "Received: {}\t"
                    "Current bitrate: {}".format(
                        self.totalTime,
                        self.sent,
                        self.received,
                        (self.sent * 4 * 8) // self.totalTime
                    )
                )

    def transmit(self, transmitter):
        print("Thread {} transmitting".format(threading.current_thread()))
        sent = totalTime = 0
        transmitter.stopListening()
        timer = time.monotonic()
        while True:
            buffer = struct.pack("<f", self.device.payload[0])
            result = transmitter.write(buffer)   # This line blocks <----------------
            if result:
                self.sent += 1
                self.device.payload[0] += 0.01

    def receive(self, receiver):
        print("Thread {} receiving".format(threading.current_thread())) 
        receiver.startListening()
        while True:
            hasPayload, pipeNo = receiver.available_pipe()
            if hasPayload:
                self.received += 1
                buffer = receiver.read(receiver.payloadSize)
                self.device.payload[1] = struct.unpack("<f", buffer[:4])[0]
        receiver.stopListening()

    def __init__(self, radios, role = ""):
        print("Created Duplex!")
        self.device = Device(radios, role)
        self.device.radios[0].channel = 100 if role.upper().startswith("B") else 76
        self.device.radios[1].channel = 100 if role.upper().startswith("M") else 76 # 76 is default
        self.totalTime = self.sent = self.received = 0
    