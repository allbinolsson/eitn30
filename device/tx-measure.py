import sys
import time
import struct
from base import Base
from RF24 import RF24

def measure(base, tx, endTime = 10): # this function assumes receiver is waiting to receive
    sent = 0
    tx.stopListening()
    startTime = time.monotonic()
    while time.monotonic() - startTime < endTime:
        buffer = struct.pack("<f", base.payload[0])
        result = tx.write(buffer)
        if result:
            print("Successfully sent package")
            sent += 1
            base.payload[0] += 0.01
    endTime = time.monotonic()

    # packages * bytes  * bits / time = average bps
    finalTime = endTime - startTime
    avg = (sent * tx.payloadSize * 8) / finalTime
    print(
        "Transmission time: {}s\n"
        "Packages sent: {}\n"
        "Average bits per second (BPS): {}\n".format(
            finalTime,
            sent,
            avg
        )
    )

if __name__ == '__main__':
    base = Base([RF24(17, 0), RF24(27, 10)])
    tx = base.radios[0] # as of now we transmit 4 byte floats.
                        # The transmission can be optimized

    measure(base, tx)

    base.shutDown()
    sys.exit()