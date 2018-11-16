import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from usb_hid_test import hidHelper


baba = False
def data_gen():
    usb_dev = hidHelper()
    usb_dev.start()
    laji = usb_dev.device
    if usb_dev.device:
        print(usb_dev.device.set_raw_data_handler)
        usb_dev.device.set_raw_data_handler(received)
    t = data_gen.t
    c = 0
    while c<120:
        c +=1
        t += 1
        print('ceshi y = ',y)
        yield t, y

def received(data):
    global y
    print(data)
    y = (data[3]+data[4])*np.random.rand(1)




def run(data):
    # update the data
    t, y = data
    xdata.append(t)
    ydata.append(y)
    xmin, xmax = ax.get_xlim()

    if t >= xmax:
        ax.set_xlim(xmin, 2 * xmax)
        ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,
while baba == True:
    y = None
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.set_ylim(0, 300)
    ax.set_xlim(0, 5)
    ax.grid()
    xdata, ydata = [], []
    data_gen.t = 0
    ani = animation.FuncAnimation(fig, run, data_gen, blit=True, interval=10,
                              repeat=False)
    plt.show()

