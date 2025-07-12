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



def ca_cfar_peak(signal, num_train=35, num_guard=5, pfa=5e-4, peak_guard=2):
    """CA-CFAR that returns only the local maximum of each target blob."""
    abs_x = np.abs(signal)
    n = len(signal)
    alpha = num_train * (pfa ** (-1/num_train) - 1)
    peaks = []
    for k in range(num_train + num_guard, n - num_train - num_guard):
        # 1) build threshold
        noise = np.concatenate([abs_x[k-num_guard-num_train:k-num_guard],
                                abs_x[k+num_guard+1:k+num_guard+num_train+1]])
        thresh = alpha * np.mean(noise)
        # 2) detection + local-max check (peak_guard ≈ half main-lobe width)
        if abs_x[k] > thresh and abs_x[k] == abs_x[k-peak_guard:k+peak_guard+1].max():
            peaks.append(k)
    return np.array(peaks)

