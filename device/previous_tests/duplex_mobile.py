import threading
import sys
from duplex import Duplex
from RF24 import RF24

if __name__ == '__main__':
    duplex = Duplex([RF24(17, 0), RF24(27, 10)], "M")
    transmitter = duplex.device.radios[0]
    receiver = duplex.device.radios[1]

    rx = threading.Thread(target=duplex.receive, args=(receiver,))
    rx.start()
    tx = threading.Thread(target=duplex.transmit, args=(transmitter,))
    tx.start()
    info = threading.Thread(target=duplex.printInfo, args=(1,))
    info.start()

    rx.join()
    tx.join()
    info.join()

    duplex.device.shutDown()
    sys.exit()