import random
import threading
import time
from mobile import init
from tun_device import TunDevice
from RF24 import RF24
from longgeframe import Frame, FrameReader

def setRole():
    role = ""
    while True:
        role = input("Enter device role, 'B' for base and 'M' for mobile").upper()
        if role != "B" and role != "M":
            print("Invalid input, please try again.")
        else:
            print("'{}' entered, starting device...".format(role))
            break
    return role

def generateBits(length: int, frameReader: FrameReader):
    bitString = ""
    for i in range(length):
        bitString += str(random.choice([0, 1]))
    hexString = frameReader.bits2bytes(bitString).hex()
    return bitString, hexString

def operateBase(tun: TunDevice):
    # Measure how many bits we receive, including headers
    rx = tun.radios[1]
    rx.startListening()

    data = 0
    total = 0

    startTime = 0
    endTime = 0
    while time.monotonic() - endTime <= 2 or endTime == 0:
        hasPayload, _ = rx.available_pipe()
        if hasPayload:
            if startTime == 0: startTime = time.monotonic()
            rcvd = rx.read(rx.payloadSize)
            bits = tun.fr.bytes2bits(rcvd)
            # print(bits)
            total += len(bits)
            data += len(tun.fr.data(bits))

            endTime = time.monotonic() # update end time each time we get new message

    t = endTime - startTime
    print("{} total bits in {} seconds\t:\tReceived {} bits of data".format(total, t, data))
    print("Data rates: {} bps (data rate), {} bps (throughput)".format((total / t), (data / t)))

def operateMobile(tun: TunDevice, n = 1000):
    # init(tun)
    bitsSent = 0
    startTime = time.monotonic()
    lastTime = time.monotonic() # queue test timer    

    for i in range(n):
        # msgLength = random.randint(185, 2944)   # this way we send 2-16 messages
        msgLength = 2944
        bitVal, hexVal = generateBits(msgLength, tun.fr)
        bitsSent += len(bitVal)
        tun.sendBits(bitVal)

    endTime = time.monotonic()
    t = endTime - startTime
    print("Sent {} bits in {} seconds".format(bitsSent, t))
    print("Throughput:", (bitsSent / t), "bps")

if __name__ == "__main__":
    # each data packet can contain 184 bits of data
    # there are four bits = 16 possible fragments
    # Max data per "file": 184 * 16 =  2944 bits
    
    role = setRole()
    mask = "255.255.255.0"
    tunData = ["192.168.2.1", mask] if role == "B" else ["192.168.2.2", mask]
    tun = TunDevice(tunData, [RF24(17, 0), RF24(27, 10)])

    # tThread = threading.Thread(target=tun.transmit, args=())
    # rThread = threading.Thread(target=tun.receive, args=())
    # tThread.start()
    # rThread.start()

    if role == "B": operateBase(tun)
    else: operateMobile(tun)