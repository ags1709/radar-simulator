import matplotlib.pyplot as plt
from radar.simulator import generate_pulse
import numpy as np


def plotPulse(pulse, time, title):
    # TODO: Make docstring for this function?
    plt.plot(time * 1e6, pulse)
    plt.xlabel("Time (μs)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.show()


def plot_signal_with_peaks(signal, time, peaks, title="Signal with Detected Peaks"):
    """
    Plots the signal and overlays detected peaks.

    Parameters:
    - signal: 1D array of signal values
    - time: 1D array of time values (same length as signal)
    - peaks: 1D array of indices in `signal` corresponding to detected peaks
    - title: Title for the plot
    """
    plt.figure(figsize=(12, 5))
    plt.plot(time * 1e6, signal, label="Signal")
    plt.plot(time[peaks] * 1e6, signal[peaks], 'rx', label="Detected Peaks", markersize=8)
    plt.xlabel("Time (µs)")
    plt.ylabel("Amplitude")
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
