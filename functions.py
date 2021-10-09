import matplotlib.pyplot as plt

def draw(fn, setpoint=700):
    with open(f'data/{fn}', 'r') as f:
        ypoints = list(map(lambda x: int(float(x)), f.read().split()))
    xpoints = range(len(ypoints))
    plt.plot(xpoints, ypoints, color='b')
    plt.plot(xpoints, [setpoint] * len(xpoints), color='r')
    plt.savefig(f'data/{fn}.png')
    plt.show()
