from radar.simulator import generate_pulse
from radar.targets import *
from radar.signalProcessing import *
import matplotlib.pyplot as plt
from visualizations.plotResults import *


SAMPLE_RATE = 1e9 # 1 GHz
FREQ = 1e6 # 1 MHz
DURATION = 2e-6 # 2 μs


# TODO: Throw both the transmit signal and echo visualization into a single figure

pulse, pulse_time = generate_pulse(frequency=FREQ, duration=DURATION, sample_rate=SAMPLE_RATE)
plotPulse(pulse, pulse_time, "Simulated Pulse")

targets = [
    1700,
    3930,
    6143
]

received_signal, echo_time = simulate_echoes(pulse, sample_rate=SAMPLE_RATE, targets=targets, noise_std=3e-8)
plotPulse(received_signal, echo_time, "Full Received Radar Signal")

mf_output = matched_filter(received_signal=received_signal, pulse=pulse)
plotPulse(mf_output, echo_time, "Matched Filter Output")

peaks = simple_peak_detector(mf_output, threshold=0.04, distance=2000)
plot_signal_with_peaks(mf_output, echo_time, peaks, title="Signal with Detected Peaks")

# Calculate distances
peak_times = peaks / SAMPLE_RATE  # convert from samples to time (1e6 = sample rate)

# # Convert time to distance
distances = (peak_times * 3e8) / 2  # divide by 2 for round trip
print("Detected distances (m):", distances)
