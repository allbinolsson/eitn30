import sys
from mobile import Mobile 
from RF24 import RF24

# rx = RF24(27, 10) # TODO
# tx = RF24(17, 0)

if __name__ == "__main__":
    # radio = RF24(17, 0)
    mobile = Mobile([RF24(17, 0), RF24(27, 10)], "R")

    try:
        mobile.operate()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        mobile.shutDown()
        sys.exit()
