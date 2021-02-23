import random # temp
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Plotter:
    def __init__(self):
        self.time = 0
        self.goodput = []
        self.throughput = []

        # self.animation = FuncAnimation(plt.gcf(), self.plot, interval=500)
        matplotlib.use('tkagg')
        self.plot()

    def update(self, dtime, throughput, goodput):
        self.time += dtime
        self.throughput.append(throughput)
        self.goodput.append(goodput)

    def plot(self):
        # this update is temporary
        # self.update(0.5, random.randint(0, 5), 0)
        
        # plt.cla()
        # plt.plot(list(range(self.time)), self.throughput)
        plt.plot([1, 2, 3, 4])
        plt.show()