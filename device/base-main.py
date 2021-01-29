import sys
from RF24 import RF24
from base import Base

# rx = RF24(27, 10) # TODO
# tx = RF24(17, 0)

if __name__ == "__main__":
    radio = RF24(17, 0)
    base = Base(radio, "T")

    try:
        while True:
            base.operate() 
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        base.r1.powerDown()
        sys.exit()