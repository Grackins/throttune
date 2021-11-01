import matplotlib.pyplot as plt


COLORS = 'bgmck'


def read_file(fn):
    with open(f'data/{fn}', 'r') as f:
        return list(map(lambda x: int(float(x)), f.read().split()))


def write_data(fn, data):
    with open(f'data/{fn}', 'w') as f:
        f.write('\n'.join([str(x) for x in data]))


def draw(fn, setpoint=700):
    multi_draw([fn], setpoint)


def multi_draw(fns, setpoint=700):
    longest = 0
    for i, fn in enumerate(fns):
        ypoints = read_file(fn)
        xpoints = range(len(ypoints))
        longest = max(longest, len(ypoints))
        plt.plot(xpoints, ypoints, color=COLORS[i % len(COLORS)])

    xpoints = range(longest)
    plt.plot(xpoints, [setpoint] * len(xpoints), color='r')
    plt.savefig(f'data/{fn}.png')
    plt.show()


def apply_filter(fn, nfn, filter_func):
    input_data = read_file(fn)
    output_data = list(filter_func(input_data))
    write_data(nfn, output_data)
