"""
Signal Processing Module for Radar Applications

This module implements core radar signal processing algorithms including:
- Matched filtering echo detection
- Constant False Alarm Rate (CFAR) detection
- Performance analysis utilities
"""

import numpy as np
from scipy.signal import find_peaks, windows
from typing import Tuple, Optional, Dict, List


def matched_filter(received_signal: np.ndarray, 
                  pulse: np.ndarray,
                  normalize: bool = True) -> np.ndarray:
    """
    Apply matched filtering to detect echoes in the received signal.
    
    The matched filter is the optimal linear filter for maximizing the 
    signal-to-noise ratio (SNR) in the presence of additive white noise.
    It correlates the received signal with a time-reversed, conjugated 
    copy of the transmitted pulse.
    
    Parameters
    ----------
    received_signal : np.ndarray
        The received radar signal containing echoes and noise.
    pulse : np.ndarray
        The transmitted radar pulse (reference signal).
    normalize : bool, optional
        If True, normalize the output by the pulse energy. Default is True.
    
    Returns
    -------
    np.ndarray
        Matched filter output with same length as received_signal.
    """
    # Time-reverse and conjugate the pulse
    matched_pulse = np.conjugate(pulse[::-1])
    
    # Perform convolution (correlation with time-reversed signal)
    output = np.convolve(received_signal, matched_pulse, mode='same')
    
    # Normalize by pulse energy if requested
    if normalize:
        pulse_energy = np.sum(np.abs(pulse)**2)
        output = output / pulse_energy
    
    return output


def ca_cfar_detector(signal: np.ndarray,
                    num_train: int = 35,
                    num_guard: int = 5,
                    pfa: float = 1e-3,
                    peak_guard: int = 2) -> np.ndarray:
    """
    Cell-Averaging Constant False Alarm Rate (CA-CFAR) detector.
    
    CA-CFAR maintains a constant probability of false alarm by adaptively
    setting the detection threshold based on the local noise estimate from
    surrounding cells.
    
    Parameters
    ----------
    signal : np.ndarray
        Input signal (typically matched filter output magnitude).
    num_train : int
        Number of training cells on each side for noise estimation.
    num_guard : int
        Number of guard cells on each side to exclude target energy.
    pfa : float
        Desired probability of false alarm.
    peak_guard : int
        Window size for local maximum detection (suppresses sidelobes).
    
    Returns
    -------
    np.ndarray
        Indices of detected peaks in the signal.
    """
    abs_signal = np.abs(signal)
    n = len(signal)
    
    # Calculate CFAR multiplier based on desired Pfa
    # For Gaussian noise: α = N * (Pfa^(-1/N) - 1)
    alpha = num_train * (pfa ** (-1/num_train) - 1)
    
    detected_peaks = []
    
    # Process each cell (excluding edges)
    for k in range(num_train + num_guard, n - num_train - num_guard):
        # Extract training cells (excluding guard cells)
        left_train = abs_signal[k - num_guard - num_train : k - num_guard]
        right_train = abs_signal[k + num_guard + 1 : k + num_guard + num_train + 1]
        
        # Estimate noise power (cell averaging)
        noise_cells = np.concatenate([left_train, right_train])
        noise_estimate = np.mean(noise_cells)
        
        # Calculate adaptive threshold
        threshold = alpha * noise_estimate
        
        # Detection decision with local maximum constraint
        if abs_signal[k] > threshold:
            # Check if it's a local maximum within peak_guard window
            window = abs_signal[k - peak_guard : k + peak_guard + 1]
            if abs_signal[k] == np.max(window):
                detected_peaks.append(k)
    
    return np.array(detected_peaks)
