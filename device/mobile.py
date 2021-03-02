import threading
import ipaddress
from longgeframe import Frame, FrameReader
from tun_mobile import TunMobile
from RF24 import RF24

if __name__ == "__main__":
    tun = TunMobile(["192.168.2.2", "255.255.255.0"], # gateway="192.168.2.1"
                    [RF24(17, 0), RF24(27, 10)])
                    # ["192.168.10.215", "192.168.10.200", 4000])
    tun.radios[1].startListening()  # To send initial frame

    # Send initial frame to base station
    initFrame = Frame(1, 0, 0, 0, 0, format(int(ipaddress.IPv4Address(tun.ip)), "032b"))
    frameVal = initFrame.compile()
    tun.radios[0].write(tun.fr.bits2bytes(frameVal))
    
    hasPayload = False
    while not hasPayload:
        hasPayload, pipeNo = tun.radios[1].available_pipe()
        if hasPayload:
            rcvd = tun.radios[1].read(tun.radios[1].payloadSize)
            bits = tun.fr.bytes2bits(rcvd)
            fragment = tun.fr.fragment(bits)
            data = tun.fr.data(bits)
            tun.handshake(fragment, int(data, 2))

    # Start threads to continously look for packages
    rxThread = threading.Thread(target=tun.receive, args=())
    txThread = threading.Thread(target=tun.transmit, args=())
    
    rxThread.start()
    txThread.start()
    
    # tun.close()