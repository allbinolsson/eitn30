class FrameReader:
    def plane(self, frame):
        return int(frame.decode()[2], 2)

    def fragment(self, frame):
        return int(frame[3:5], 2)

    def data(self, frame):
        return int(frame[5:], 2)

class Frame:
    def __init__(self, plane = 0, fragment = 0, data = 0):
        self.plane = plane          # 0 for data, 1 for control
        self.fragment = fragment    # fragments used for control, 2 bits long
        self.data = data

    def setControl(self, fragment = 0):
        self.plane = 1
        self.fragment = fragment
    
    def addData(self, data: int):
        self.data = data
    

    def getFrame(self):
        frame = format(self.plane, "#b")

        frame += format(self.fragment, "02b")

        frame += format(self.data, "032b")

        return frame