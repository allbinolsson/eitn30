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

radio = RF24(27, 10)
# rx = RF24(27, 10) # TODO
# tx = RF24(17, 0)

payload = [0.0]

def receive(timeout=6):
    radio.startListening()  # put radio in RX mode

    start_timer = time.monotonic()
    while (time.monotonic() - start_timer) < timeout:
        has_payload, pipe_number = radio.available_pipe()
        if has_payload:
            # fetch 1 payload from RX FIFO
            buffer = radio.read(radio.payloadSize)
            # use struct.unpack() to convert the buffer into usable data
            # expecting a little endian float, thus the format string "<f"
            # buffer[:4] truncates padded 0s in case payloadSize was not set
            payload[0] = struct.unpack("<f", buffer[:4])[0]
            # print details about the received packet
            print(
                "Received {} bytes on pipe {}: {}".format(
                    radio.payloadSize,
                    pipe_number,
                    payload[0]
                )
            )
            start_timer = time.monotonic()  # reset the timeout timer

    print("Nothing received in 6 seconds. Leaving RX role")
    # recommended behavior is to keep in TX mode while idle
    radio.stopListening()  # put the radio in TX mode


def operate():
    user_input = input(
        "*** Enter 'R' for receiver role.\n"
        "*** Enter 'Q' to quit example.\n"
    ) or "?"
    user_input = user_input.split()
    if user_input[0].upper().startswith("R"):
        if len(user_input) > 1:
            receive(int(user_input[1]))
        else:
            receive()
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
    # It is very helpful to think of an address as a path instead of as
    # an identifying device destination

    print(sys.argv[0])  # print example name

    # to use different addresses on a pair of radios, we need a variable to
    # uniquely identify which address this radio will use to transmit
    # 0 uses address[0] to transmit, 1 uses address[1] to transmit
    radio_number = args.node  # uses default value from `parser`
    if args.node is None:  # if '--node' arg wasn't specified
        radio_number = 1

    radio.setPALevel(RF24_PA_LOW)  # RF24_PA_MAX is default
    radio.openWritingPipe(address[radio_number])  # always uses pipe 0
    radio.openReadingPipe(1, address[not radio_number])  # using pipe 1
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
            if not bool(args.role): receive()
    except KeyboardInterrupt:
        print(" Keyboard Interrupt detected. Exiting...")
        radio.powerDown()
        sys.exit()
