from radar.simulator import generate_pulse
from radar.targets import *
from radar.signalProcessing import matched_filter
import matplotlib.pyplot as plt
from visualizations.plotResults import *


SAMPLE_RATE = 10e8 # 100 MHz
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

received_signal, echo_time = simulate_echoes(pulse, sample_rate=SAMPLE_RATE, targets=targets, noise_std=1e-8)
plotPulse(received_signal, echo_time, "Full Received Radar Signal")

mf_output = matched_filter(received_signal=received_signal, pulse=pulse)
plotPulse(mf_output, echo_time, "Matched Filter Output")

# ---------------------------------------------------------------------------------------------
# Calculate distances

# from scipy.signal import find_peaks
# print(f"Filtered output: {mf_output}")
# peaks, _ = find_peaks(mf_output, height=1e-6)  # Tune threshold
# print(f"Peaks: {peaks}")
# peak_times = peaks / SAMPLE_RATE  # convert from samples to time (1e6 = sample rate)

# # Convert time to distance
# distances = (peak_times * 3e8) / 2  # divide by 2 for round trip
# print("Detected distances (m):", distances)
