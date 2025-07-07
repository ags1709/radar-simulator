from radar.simulator import generate_pulse
from radar.targets import *
import matplotlib.pyplot as plt
from visualizations.plotResults import *

SAMPLE_RATE = 1e8 # 100 MHz
FREQ = 1e6 # 1 MHz
DURATION = 2e-6 # 2 μs


# TODO: Throw both the transmit signal and echo visualization into a single figure

pulse, pulse_time = generate_pulse(frequency=FREQ, duration=DURATION, sample_rate=SAMPLE_RATE)
plotPulse(pulse, pulse_time, "Simulated Pulse")


targets = [
    (1700, 1.0),
    (3930, 1.0),
    (6143, 1.0)
]

received_signal, echo_time = simulate_echoes(pulse, sample_rate=SAMPLE_RATE, targets=targets, noise_std=0)
plotPulse(received_signal, echo_time, "Full Received Radar Signal (Echoes)")

