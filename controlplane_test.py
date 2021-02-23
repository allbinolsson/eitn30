import ipaddress

class FrameReader:
    def plane(self, frame):
        return frame[2]

    def fragment(self, frame):
        return frame[3:5]

    def data(self, frame):
        return int(frame[5:], 2)

class Frame:
    def __init__(self):
        self.plane = 0
        self.fragment = None
        self.data = 0

    def setControl(self):
        self.plane = 1
        self.fragment = 0
    
    def addData(self, data: int):
        self.data = data
        
    def getFrame(self):
        frame = format(self.plane, "#b")

        frame += format(self.fragment, "02b")

        frame += format(self.data, "032b")

        return frame

def setFrame(plane, frag, data):
    frame = Frame()
    if plane: frame.setControl()
    if plane: frame.fragment = frag
    frame.addData(data)
    return frame

if __name__ == "__main__":
    frame = Frame()
    fr = FrameReader()
    
    frame.setControl()
    frameValue = frame.getFrame()
    
    readings = [fr.plane(frameValue), fr.fragment(frameValue), fr.data(frameValue)]
    print(readings)

    # so far so good ---------------------------------------------------------------
    # let's try a handshake

    ip = int(ipaddress.ip_address("192.168.2.2"))
    print(ip)
    f0 = setFrame(1, 0, ip) # received by base
    val = f0.getFrame()
    print("ip received:", ipaddress.IPv4Address(fr.data(val)))

    newIp = int(ipaddress.ip_address("192.168.2.3"))
    f1 = setFrame(1, 1, newIp)
    val = f1.getFrame()
    print(val, type(val))