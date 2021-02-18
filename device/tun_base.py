import threading
from tun_device import TunDevice

if __name__ == "__main__":
    tun = TunDevice(["192.168.2.1", "255.255.255.0"],
                    ["192.168.10.200", "192.168.10.215", 4000])
    
    rxThread = threading.Thread(target=tun.receive, args=())
    txThread = threading.Thread(target=tun.transmit, args=())
    rxThread.start()
    txThread.start()

    # tun.close()