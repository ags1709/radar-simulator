import numpy as np



def generate_pulse(frequency=5e3, duration=1e-3, sample_rate=1e6):
    # Simulate
    t = np.arange(0, duration, 1/sample_rate)
    pulse = np.sin(2 * np.pi * frequency * t)
    return pulse, t

pulse, time = generate_pulse()

