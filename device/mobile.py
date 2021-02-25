import threading
import ipaddress
from longgeframe import Frame, FrameReader
from tun_mobile import TunMobile

if __name__ == "__main__":
    tun = TunMobile(["192.168.2.2", "255.255.255.0"], # gateway="192.168.2.1"
                    ["192.168.10.215", "192.168.10.200", 4000])

    initFrame = Frame(1, 0, int(ipaddress.IPv4Address(tun.ip)))
    frameVal = initFrame.getFrame()
    tun.txSocket.sendto(frameVal.encode(), (tun.UDP[1], tun.UDP[2]))
    print("Sent initial frame!")

    rcvd, addr = tun.rxSocket.recvfrom(1024)
    fragment = tun.fr.fragment(rcvd)
    data = tun.fr.data(rcvd)
    tun.handshake(fragment, data)

    rxThread = threading.Thread(target=tun.receive, args=())
    txThread = threading.Thread(target=tun.transmit, args=())
    rxThread.start()
    txThread.start()
    
    # tun.close()