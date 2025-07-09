from scipy.signal import find_peaks
import numpy as np




def matched_filter(received_signal, pulse):
    """
    Apply matched filtering to detect echoes in the received signal.
    
    Parameters:
    - received_signal: 1D numpy array (the echo signal)
    - pulse: The transmitted radar pulse (same one you generated earlier)
    
    Returns:
    - output: Matched filter output (correlation result)
    """
    # Time-reverse and conjugate the pulse (real signal so conjugate = same)
    matched_pulse = np.conjugate(pulse[::-1])
    # conjugate = np.conjugate(matched_pulse)
    
    # Calculate convolution of received signal with matched pulse
    output = np.convolve(received_signal, matched_pulse, mode='same')
    return output




def simple_peak_detector(signal, threshold=0.07, distance=100):
    """
    Find strong peaks above threshold, separated by some minimum distance.
    """
    abs_signal = np.abs(signal)
    norm = abs_signal / np.max(abs_signal)
    peaks, _ = find_peaks(norm, height=threshold, distance=distance)
    return peaks




def simple_cfar(signal, num_train=10, num_guard=2, rate=5):
    """
    Simple 1D CFAR detector
    """
    n = len(signal)
    peaks = []

    for i in range(num_train + num_guard, n - num_train - num_guard):
        # Training cells on both sides, excluding guard cells
        training_cells = np.concatenate([
            np.abs(signal[i - num_train - num_guard:i - num_guard]),
            np.abs(signal[i + num_guard:i + num_guard + num_train])
        ])
        noise_level = np.mean(training_cells)
        # noise_level = np.median(training_cells)
        threshold = rate * noise_level  # scaling factor

        if np.abs(signal[i]) > threshold:
            peaks.append(i)
    
    return np.array(peaks)





