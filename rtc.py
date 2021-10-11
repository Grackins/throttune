from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation


class RTCDrawer:
    def __init__(self, buf):
        self.buf = buf

    def draw(self):
        fig, ax = plt.subplots()
        ln, = plt.plot([], [], color='b')

        def init():
            ax.set_ylim(0, 1024)
            return ln,

        def update(frame):
            ydata = self.buf[-10000:]
            xdata = range(len(self.buf))[-10000:]
            ln.set_data(xdata, ydata)
            if xdata:
                ax.set_xlim(xdata[-1] - 10000, xdata[-1])
            return ln,

        self.ani = FuncAnimation(
            fig,
            update,
            init_func=init,
            interval=50,
        )
        plt.show()
