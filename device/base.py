import threading
from tun_base import TunBase
from RF24 import RF24

if __name__ == "__main__":
    tun = TunBase(["192.168.2.1", "255.255.255.0"],
                    [RF24(17, 0), RF24(27, 10)])
                    # ["192.168.10.200", "192.168.10.215", 4000])

    rxThread = threading.Thread(target=tun.receive, args=())
    txThread = threading.Thread(target=tun.transmit, args=())
    
    rxThread.start()
    txThread.start()

    # tun.close()