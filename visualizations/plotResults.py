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



def plot_complex_pulse(pulse, t, title="Complex Pulse"):
    fig, ax = plt.subplots(3, 1, sharex=True, figsize=(10, 6))

    # (1) I and Q channels
    ax[0].plot(t*1e6, np.real(pulse), label="Real (I)")
    ax[0].plot(t*1e6, np.imag(pulse), label="Imag (Q)", alpha=0.7)
    ax[0].set_ylabel("Amplitude")
    ax[0].legend(loc="upper right")
    ax[0].set_title(title + " – I/Q components")

    # (2) Envelope
    ax[1].plot(t*1e6, np.abs(pulse))
    ax[1].set_ylabel("|s(t)|")

    # (3) Instantaneous frequency f(t) = 1/(2π) · dφ/dt
    phase = np.unwrap(np.angle(pulse))
    inst_freq = np.diff(phase) / (2*np.pi*np.diff(t))
    ax[2].plot(t[1:]*1e6, inst_freq/1e6)      # MHz for readability
    ax[2].set_ylabel("f_inst [MHz]")
    ax[2].set_xlabel("Time [µs]")

    fig.tight_layout()
    plt.show()
