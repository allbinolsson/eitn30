import struct
import time
from RF24 import RF24, RF24_PA_LOW

class Device:
    def __init__(self, radios, role):
        self.radios = radios
        self.payload = [0.0]
        self.address = [b'1Node', b'2Node']
        self.role = role if role.upper().startswith("T") or role.upper().startswith("R") else "?"
        for r in self.radios:
            if not r.begin():
                raise RuntimeError("radio hardware is not responding")
            r.setPALevel(RF24_PA_LOW)
            r.openWritingPipe(self.address[self.radio_number])
            r.openReadingPipe(1, self.address[not self.radio_number])
            r.payloadSize = len(struct.pack("<f", self.payload[0]))
            

    def transmit(self):  
        """Transmits an incrementing float every second"""
        tx = self.radios[0]
        tx.stopListening()  # put radio in TX mode
        while True:
            buffer = struct.pack("<f", self.payload[0])
            start_timer = time.monotonic_ns()  # start timer
            result = tx.write(buffer)
            end_timer = time.monotonic_ns()  # end timer
            if not result:
                print("Transmission failed or timed out")
            else:
                print(
                    "Transmission successful! Time to Transmit: "
                    "{} us. Sent: {}".format(
                        (end_timer - start_timer) / 1000,
                        self.payload[0]
                    )
                )
                self.payload[0] += 0.01
        print(failures, "failures detected. Leaving TX role.")

    def receive(self, timeout=6):
        print("Starting RX device.")
        rx = self.radios[1]
        rx.startListening()  # put radio in RX mode
        
        while True:
            has_payload, pipe_number = rx.available_pipe()
            if has_payload:
                # fetch 1 payload from RX FIFO
                buffer = rx.read(rx.payloadSize)
                self.payload[0] = struct.unpack("<f", buffer[:4])[0]
                print(
                    "Received {} bytes on pipe {}: {}".format(
                        rx.payloadSize,
                        pipe_number,
                        self.payload[0]
                    )
                )
        # recommended behavior is to keep in TX mode while idle
        rx.stopListening()

    def operate(self):
        if self.role.upper().startswith("T"):   self.transmit()
        elif self.role.upper().startswith("R"):  self.receive()
        else:   print("Invalid device role.")

    def shutDown (self):
        for r in self.radios:
            r.powerDown()