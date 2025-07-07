import matplotlib.pyplot as plt
from radar.simulator import generate_pulse


def plotPulse(pulse, time, title):
    # TODO: Make docstring for this function?
    plt.plot(time * 1e6, pulse)
    plt.xlabel("Time (μs)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.show()