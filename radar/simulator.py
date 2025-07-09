import numpy as np



def generate_pulse(frequency=5e3, duration=0.1e-3, sample_rate=1e6):
    # TODO: Make docstring for this function
    # Simulate transmit signal of a radar system
    # Basic sine wave used for simplicity. 
    t = np.arange(0, duration, 1/sample_rate)
    pulse = np.sin(2 * np.pi * frequency * t)
    return pulse, t




def generate_lfm_pulse(start_freq=0.0, bandwidth=20e6, duration=10e-6,
                       sample_rate=100e6, window='hanning'):
    """
    Generate a base-band linear-FM (chirp) pulse.

    Parameters
    ----------
    start_freq : float
        Base-band start frequency (Hz). Use 0 for symmetric ±B/2 sweep.
    bandwidth  : float
        Sweep bandwidth (Hz).
    duration   : float
        Pulse length (s).
    sample_rate: float
        Sampling frequency (Hz) – must be ≥ 2·(start_freq+bandwidth).
    window     : str | None
        Optional window to taper the pulse and lower sidelobes
        ('hanning', 'blackman', None).

    Returns
    -------
    pulse : complex ndarray
        Complex base-band samples of the chirp.
    t     : ndarray
        Time axis (s).
    """
    t = np.arange(0, duration, 1 / sample_rate)
    k = bandwidth / duration
    phase = 2 * np.pi * (start_freq * t + 0.5 * k * t**2)
    pulse = np.exp(1j * phase)          # complex envelope

    if window is not None:
        w = getattr(np, window)(len(t))
        pulse *= w

    # Energy-normalise so that |pulse|^2 sums to 1
    # pulse /= np.sqrt(np.sum(np.abs(pulse)**2))

    return pulse, t
