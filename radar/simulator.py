import numpy as np
from typing import Tuple, Optional


def generate_lfm_pulse(start_freq: float = 0.0,
                      bandwidth: float = 20e6,
                      duration: float = 10e-6,
                      sample_rate: float = 100e6,
                      window: Optional[str] = 'hanning',
                      up_chirp: bool = True) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a Linear Frequency Modulation (LFM) chirp pulse.
    
    LFM is the most common pulse compression waveform in radar systems,
    providing good range resolution and Doppler tolerance. The instantaneous
    frequency sweeps linearly from start_freq to (start_freq + bandwidth).
    
    Parameters
    ----------
    start_freq : float
        Starting frequency in Hz. 
    bandwidth : float
        Frequency sweep bandwidth in Hz (default 20 MHz).
    duration : float
        Pulse duration in seconds (default 10 μs).
    sample_rate : float
        Sampling frequency in Hz (default 100 MHz).
    window : str or None
        Window function to reduce sidelobes. Options: 'hanning', 'hamming',
        'blackman', or None (default 'hanning').
    up_chirp : bool
        If True, frequency increases with time (up-chirp).
        If False, frequency decreases (down-chirp).
    
    Returns
    -------
    tuple
        (pulse, time_axis) where pulse is the complex baseband signal.
    """

    # Generate time axis
    t = np.arange(0, duration, 1/sample_rate)
    n_samples = len(t)
    
    # Calculate chirp rate
    if up_chirp:
        k = bandwidth / duration  # Hz/s
    else:
        k = -bandwidth / duration
    
    # Generate chirp phase
    phase = 2 * np.pi * (start_freq * t + 0.5 * k * t**2)
    
    # Generate complex chirp
    pulse = np.exp(1j * phase)
    
    # Apply window function if specified
    if window is not None:
        if window.lower() == 'hanning':
            w = np.hanning(n_samples)
        elif window.lower() == 'hamming':
            w = np.hamming(n_samples)
        elif window.lower() == 'blackman':
            w = np.blackman(n_samples)
        else:
            raise ValueError(f"Unknown window type: {window}")
        
        pulse *= w
    
    return pulse, t
