import numpy as np


def simulate_echoes(pulse, sample_rate, targets, noise_std=0.0):
    """
    Simulates radar echoes from multiple targets.
    
    Parameters:
    - pulse: Transmitted pulse (1D numpy array)
    - sample_rate: Samples per second
    - targets: List of (distance_in_meters, amplitude) tuples
    - noise_std: Standard deviation of Gaussian noise
    
    Returns:
    - received_signal: Signal containing delayed, scaled echoes
    - t: Time axis
    """

    max_distance = max([d for d in targets])
    max_delay = 2 * max_distance / 3e8
    duration = 5e-6 + max_delay + len(pulse) / sample_rate
    total_samples = int(duration * sample_rate)

    received_signal = np.zeros(total_samples)

    for distance in targets:
        
        amplitude = 1 / ((2 * distance) ** 2) # Attenuate signal strength proportional to distance traveled

        delay = 2 * distance / 3e8
        delay_samples = int(delay * sample_rate)

        if delay_samples + len(pulse) > total_samples:
            continue
        
        # Add scaled, delayed pulse
        received_signal[delay_samples:delay_samples+len(pulse)] += amplitude * pulse

    # Add noise
    if noise_std > 0.0:
        received_signal += np.random.normal(0, noise_std, size=received_signal.shape)

    t = np.arange(0, len(received_signal)) / sample_rate

    return received_signal, t
