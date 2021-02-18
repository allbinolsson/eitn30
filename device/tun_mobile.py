import threading
from tun_device import TunDevice

RCV_IP = "192.168.10.200"
MY_IP = "192.168.10.215"
UDP_PORT = 4000

if __name__ == "__main__":
    tun = TunDevice(["192.168.2.2", "255.255.255.0"], # gateway="192.168.2.1"
                    ["192.168.10.215", "192.168.10.200", 4000])

    rxThread = threading.Thread(target=tun.receive, args=())
    txThread = threading.Thread(target=tun.transmit, args=())
    rxThread.start()
    txThread.start()

    # tun.close()