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
    matched_pulse = pulse[::-1]
    
    # Calculate convolution of received signal with matched pulse
    output = np.convolve(received_signal, matched_pulse, mode='same')
    return output
