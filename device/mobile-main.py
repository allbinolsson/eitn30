import sys
from mobile import Mobile 
from RF24 import RF24, RF24_PA_LOW

# rx = RF24(27, 10) # TODO
# tx = RF24(17, 0)

if __name__ == "__main__":
    radio = RF24(17, 0)
    mobile = Mobile(radio, "R")

    try:
        while True:
            mobile.operate()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        mobile.r1.powerDown()
        sys.exit()
