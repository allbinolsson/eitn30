import sys
from RF24 import RF24
from base import Base

# rx = RF24(27, 10) # TODO
# tx = RF24(17, 0)

if __name__ == "__main__":
    #radio = RF24(17, 0)
    base = Base([RF24(17, 0), RF24(27, 10)], "T")

    try:
        base.operate()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        base.shutDown()
        sys.exit()