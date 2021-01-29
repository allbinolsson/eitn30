import struct
import time
from RF24 import RF24, RF24_PA_LOW

class Device:
    def __init__(self, r1, role):
        self.r1 = r1
        self.payload = [0.0]
        if not self.r1.begin():
            raise RuntimeError("radio hardware is not responding")
        self.address = [b'1Node', b'2Node']
        self.role = role if role.upper().startswith("T") or role.upper().startswith("R") else "?"

        print("radio number:", self.radio_number)
        self.r1.setPALevel(RF24_PA_LOW)
        self.r1.openWritingPipe(self.address[self.radio_number])
        self.r1.openReadingPipe(1, self.address[not self.radio_number])
        self.r1.payloadSize = len(struct.pack("<f", self.payload[0]))

    def transmit(self):
        """Transmits an incrementing float every second"""
        self.r1.stopListening()  # put radio in TX mode
        failures = 0
        while failures < 6:
            buffer = struct.pack("<f", self.payload[0])
            start_timer = time.monotonic_ns()  # start timer
            result = self.r1.write(buffer)
            end_timer = time.monotonic_ns()  # end timer
            if not result:
                print("Transmission failed or timed out")
                failures += 1
            else:
                print(
                    "Transmission successful! Time to Transmit: "
                    "{} us. Sent: {}".format(
                        (end_timer - start_timer) / 1000,
                        self.payload[0]
                    )
                )
                self.payload[0] += 0.01
            time.sleep(1)
        print(failures, "failures detected. Leaving TX role.")

    def receive(self, timeout=6):
        print("Starting RX device.")
        self.r1.startListening()  # put radio in RX mode

        start_timer = time.monotonic()
        while (time.monotonic() - start_timer) < timeout:
            has_payload, pipe_number = self.r1.available_pipe()
            if has_payload:
                # fetch 1 payload from RX FIFO
                buffer = self.r1.read(self.r1.payloadSize)
                self.payload[0] = struct.unpack("<f", buffer[:4])[0]
                print(
                    "Received {} bytes on pipe {}: {}".format(
                        self.r1.payloadSize,
                        pipe_number,
                        self.payload[0]
                    )
                )
                start_timer = time.monotonic()  # reset the timeout timer
        # recommended behavior is to keep in TX mode while idle
        self.r1.stopListening()

    def operate(self):
        if self.role.upper().startswith("T"):   self.transmit()
        elif self.role.upper().startswith("R"):  self.receive()
        else:   print("Invalid device role.")