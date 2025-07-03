import matplotlib.pyplot as plt
from radar.simulator import generate_pulse


def plotPulse(pulse, time):
    plt.plot(time, pulse)
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")
    plt.title("Simulated Pulse")
    plt.grid(True)
    plt.show()

def plotSeveralPulses(frequencies):
    for f in frequencies:
        pulse, time = generate_pulse(frequency=f)
        plt.plot(time * 1e3, pulse, label=f"{f/1e3} kHz")

    plt.legend()
    plt.xlabel("Time (ms)")
    plt.ylabel("Amplitude")
    plt.title("Pulse at Different Frequencies")
    plt.grid(True)
    plt.show()
