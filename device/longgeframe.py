import ipaddress

class FrameReader:
    def bits2bytes (self, bits: str):
        return bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))

    def bytes2bits (self, byte: bytes):
        final = "" 
        for i, b in enumerate(byte):
            allZeros = True
            
            for j in range(i, len(byte)):
                if byte[j] != 0:
                    allZeros = False
            if not allZeros:
                final += format(b, "08b")
            else:
                break
        if self.plane(final) == 1:
            final = final[:40]
        return final

    def plane(self, frame):
        return int(frame[0:3], 2)

    def final(self, frame):
        return int(frame[3:4], 2)

    def fragment(self, frame):
        val = frame[4:8]
        return int(val, 2)

    def sender(self, frame):
        if self.plane(frame) == 0:
            return int(frame[8:40], 2)
        return None
    
    def receiver(self, frame):
        if self.plane(frame) == 0:
            return int(frame[40:72], 2)
        return None
    
    def data(self, frame):
        val = ""
        if self.plane(frame) == 0:
            val = frame[72:]
        else:
            val = frame[8:]
        return val


class Frame:
    DATA_LENGTH = 184
    MAX_DATA = 2**184 - 1

    def __init__(self, plane, final, fragment, sender, receiver, data: str):
        self.plane = plane
        self.final = final
        self.fragment = fragment
        self.sender = sender
        self.receiver = receiver
        self.data = data

    def compile(self):  # the fields add up to 32 bytes
        frame = format(self.plane, "03b")
        frame += format(self.final, "b")
        frame += format(self.fragment, "04b") 
        if self.plane == 0:     # data plane
            frame += format(self.sender, "032b")
            frame += format(self.receiver, "032b")
        frame += self.data
        return frame

# This main is for testing
if __name__ == "__main__":
    fr = FrameReader()

    sender = int(ipaddress.IPv4Address("192.168.2.2"))
    receiver = int(ipaddress.IPv4Address("192.168.2.1"))

    # frame = Frame(1, 14, sender, receiver, Frame.MAX_DATA)
    frame = Frame(0, 1, 0, 0, 0, format(sender, "b"))
    frameVal = frame.compile()
    print("Received frame:", frameVal, "with legnth:", len(frameVal))

    byte = fr.bits2bytes(frameVal)
    print("Hex representation:", byte, type(byte))

    bits = fr.bytes2bits(byte)
    print("reversed to bits:", bits)

    plane = fr.plane(frameVal)
    final = fr.final(frameVal)
    frag = fr.fragment(frameVal)
    s = fr.sender(frameVal)
    r = fr.receiver(frameVal)
    rData = fr.data(frameVal)

    print("plane:", plane)
    print("final:", final)
    print("fragemnt:", frag)
    if plane == 0:
        print("sender:", s , " : ", ipaddress.IPv4Address(s))
        print("receiver:", r, " : ", ipaddress.IPv4Address(r))
    print("data:", rData, ":", str(ipaddress.IPv4Address(int(rData, 2))))
    print("Data length:", len(frameVal), "bits /", len(frameVal) // 8, "bytes")