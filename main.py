from radar.simulator import *
from radar.targets import *
from radar.signalProcessing import *
import matplotlib.pyplot as plt
from visualizations.plotResults import *


# SAMPLE_RATE = 1e9 # 1 GHz
# FREQ = 1e6 # 1 MHz
# DURATION = 2e-6 # 2 μs

SAMPLE_RATE = 100e6       # 100 MHz ≥ 2·(B/2)=50 MHz
BANDWIDTH   = 20e6        # 20 MHz sweep
DURATION    = 10e-6       # 10 µs pulse

# TODO: Throw both the transmit signal and echo visualization into a single figure

# pulse, pulse_time = generate_pulse(frequency=FREQ, duration=DURATION, sample_rate=SAMPLE_RATE)
pulse, t_pulse = generate_lfm_pulse(
        start_freq=-BANDWIDTH/2,   # symmetric ±10 MHz sweep
        bandwidth=BANDWIDTH,
        duration=DURATION,
        sample_rate=SAMPLE_RATE,
        window="hanning")


plotPulse(pulse, t_pulse, "Simulated Pulse")

targets = [
    1700,
    3930,
    6027,
    7291,
]

received_signal, echo_time = simulate_echoes(pulse, sample_rate=SAMPLE_RATE, targets=targets, noise_std=3e-7)
plotPulse(received_signal, echo_time, "Received Radar Signal (Single Pulse)")

mf_out = matched_filter(received_signal=received_signal, pulse=pulse)
plotPulse(mf_out, echo_time, "Matched Filter Output (Single Pulse)")

# Use several pulses and add them together to help raise signal out of noise
N_pulses = 128
range_lines = []
for _ in range(N_pulses):
    echoes, _ = simulate_echoes(pulse, sample_rate=SAMPLE_RATE, targets=targets, noise_std=3e-7)
    range_lines.append(matched_filter(echoes, pulse))
rd_matrix = np.vstack(range_lines)          # shape (N_pulses, N_rng)
integrated = np.sum(rd_matrix, axis=0)      # coherent sum
plotPulse(integrated, echo_time, "Matched Filter Output after pulse integration")


# peaks = simple_peak_detector(integrated, threshold=0.07, distance=20)
peaks = ca_cfar_peak(signal=integrated, num_train=35, num_guard=5, pfa=8e-3, peak_guard=2)
# peaks = simple_cfar(signal=integrated, num_train=100, num_guard=2, rate=5)
plot_signal_with_peaks(integrated, echo_time, peaks, title="Final Signal with Detected Peaks")


# Since we are detecting echoes as the center of the matched filtered pulse, we will need to correct for that.
# Correct for matched filter delay
correction_samples = len(pulse) // 2
corrected_peaks = peaks - correction_samples

# Filter out any negative peak indices (they may arise at the very start)
corrected_peaks = corrected_peaks[corrected_peaks >= 0]

# Convert corrected indices to time
peak_times = corrected_peaks / SAMPLE_RATE  # seconds

# Convert to distance (meters)
distances = (peak_times * 3e8) / 2  # divide by 2 for round trip


print("Detected distances (m):", distances)

delta = np.array(targets) - np.array(distances)
print(f"Distance error: {delta}")

