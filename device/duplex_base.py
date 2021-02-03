import threading
import sys
from duplex import Duplex
from RF24 import RF24

if __name__ == '__main__':
    duplex = Duplex([RF24(17, 0), RF24(27, 10)], "B")
    transmitter = duplex.device.radios[0]
    receiver = duplex.device.radios[1]

    tx = threading.Thread(target=duplex.transmit, args=(transmitter,))    
    tx.start()

    rx = threading.Thread(target=duplex.receive, args=(receiver,))
    rx.start()
    
    info = threading.Thread(target=duplex.printInfo, args=(1,))
    info.start()

    tx.join()   # this point will never be reached because of while(true) loops
    rx.join()
    info.join()

    duplex.device.shutDown()
    sys.exit()