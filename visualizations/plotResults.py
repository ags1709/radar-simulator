import matplotlib.pyplot as plt



def plotPulse(pulse, time):
    plt.plot(time, pulse)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title("Simulated Pulse")
    plt.grid(True)
    plt.show()