import sys
import argparse
import time
import struct
from RF24 import RF24, RF24_PA_LOW


parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter
)
parser.add_argument(
    "-n",
    "--node",
    type=int,
    choices=range(2),
    help="the identifying radio number (or node ID number)"
)
parser.add_argument(
    "-r",
    "--role",
    type=int,
    choices=range(2),
    help="'1' specifies the TX role. '0' specifies the RX role."
)

radio = RF24(17, 0)
# rx = RF24(27, 10) # TODO
# tx = RF24(17, 0)

payload = [0.0]

def transmit():
    """Transmits an incrementing float every second"""
    radio.stopListening()  # put radio in TX mode
    failures = 0
    while failures < 6:
        # use struct.pack() to packet your data into the payload
        # "<f" means a single little endian (4 byte) float value.
        buffer = struct.pack("<f", payload[0])
        start_timer = time.monotonic_ns()  # start timer
        result = radio.write(buffer)
        end_timer = time.monotonic_ns()  # end timer
        if not result:
            print("Transmission failed or timed out")
            failures += 1
        else:
            print(
                "Transmission successful! Time to Transmit: "
                "{} us. Sent: {}".format(
                    (end_timer - start_timer) / 1000,
                    payload[0]
                )
            )
            payload[0] += 0.01
        time.sleep(1)
    print(failures, "failures detected. Leaving TX role.")

def operate():
    user_input = input(
        "*** Enter 'T' for transmitter role.\n"
        "*** Enter 'Q' to quit example.\n"
    ) or "?"
    user_input = user_input.split()
    if user_input[0].upper().startswith("T"):
        transmit()
        return True
    elif user_input[0].upper().startswith("Q"):
        radio.powerDown()
        return False
    print(user_input[0], "is an unrecognized input. Please try again.")
    return operate()


if __name__ == "__main__":

    args = parser.parse_args()  # parse any CLI args

    # initialize the nRF24L01 on the spi bus
    if not radio.begin():
        raise RuntimeError("radio hardware is not responding")

    # For this example, we will use different addresses
    # An address need to be a buffer protocol object (bytearray)
    address = [b"1Node", b"2Node"]

    print(sys.argv[0])  # print example name

    # to use different addresses on a pair of radios, we need a variable to
    # uniquely identify which address this radio will use to transmit
    radio_number = args.node  
    if args.node is None: 
        radio_number = 0

    # set the Power Amplifier level to -12 dBm since short distance
    radio.setPALevel(RF24_PA_LOW)  

    # set the TX address of the RX node into the TX pipe
    radio.openWritingPipe(address[radio_number]) 

    # set the RX address of the TX node into a RX pipe
    radio.openReadingPipe(1, address[not radio_number])  # using pipe 1
    
    # struct.pack(); "<f" means a little endian unsigned float
    radio.payloadSize = len(struct.pack("<f", payload[0]))

    # for debugging, we have 2 options that print a large block of details
    # (smaller) function that prints raw register values
    # radio.printDetails()
    # (larger) function that prints human readable data
    # radio.printPrettyDetails()

    try:
        if args.role is None:  # if not specified with CLI arg '-r'
            while operate():
                pass  # continue example until 'Q' is entered
        else: 
            # run role once and exit
            if bool(args.role): transmit()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        radio.powerDown()
        sys.exit()