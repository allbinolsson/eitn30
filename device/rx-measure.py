import sys
import struct
import time
from mobile import Mobile
from RF24 import RF24

def measure(mobile, rx, endTime = 10):
    # Start measuring time at first package received.
    # Continue receiving for 10 seconds
    rx.startListening()
    startTime = received = 0
    while time.monotonic() - startTime < endTime or startTime == 0:
        hasPayload, pipeNo = rx.available_pipe()
        if hasPayload:
            if startTime == 0:   startTime = time.monotonic()
            received += 1
            buffer = rx.read(rx.payloadSize)
            mobile.payload[0] = struct.unpack("<f", buffer[:4])[0]
    endTime = time.monotonic()
    finalTime = endTime - startTime
    avg = (received * rx.payloadSize * 8) / finalTime

    print(
        "Transmission time: {}\n"
        "Packages Received: {}\n"
        "Average bits per second (BPS): {}\n".format(
            finalTime,
            received,
            avg               
        )
    )

    rx.stopListening()

if __name__ == '__main__':
    mobile = Mobile([RF24(17, 0), RF24(27, 10)])
    rx = mobile.radios[1]

    measure(mobile, rx)

    mobile.shutDown()
    sys.exit()