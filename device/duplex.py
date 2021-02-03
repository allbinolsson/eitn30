import threading
import time
import struct
from device import Device

class Duplex:
    def transmit(self, transmitter):
        print("Thread {} transmitting".format(threading.current_thread()))
        sent = totalTime = 0
        transmitter.stopListening()
        timer = time.monotonic()
        while True:
            newTime = time.monotonic()
            if newTime - timer >= 1:
                timer = newTime
                totalTime += 1
                print(  
                    "Total time: {},\t"
                    "Packages sent: {},\t"
                    "Current bitrate: {} bps\n".format(
                        totalTime,
                        sent,
                        (sent * 4 * 8) // totalTime
                    )
                )
            buffer = struct.pack("<f", self.device.payload[0])
            result = transmitter.write(buffer)   # This line blocks <----------------
            if result:
                sent += 1
                self.device.payload[0] += 0.01


    def receive(self, receiver):
        print("Thread {} receiving".format(threading.current_thread())) 
        receiver.startListening()
        while True:
            hasPayload, pipeNo = receiver.available_pipe()
            if hasPayload:
                buffer = receiver.read(receiver.payloadSize)
                self.device.payload[1] = struct.unpack("<f", buffer[:4])[0]
        receiver.stopListening()

    def __init__(self, radios, role = ""):
        print("Created Duplex!")
        self.device = Device(radios, role)
        # self.mutex = threading.Lock()
        # self.condition = threading.Condition(self.mutex)
        # maybe this should be done in main (probably)
        # self.tx = threading.Thread(target = self.transmit, args = ())
        # self.rx = threading.Thread(target = self.receive, args = ())
    