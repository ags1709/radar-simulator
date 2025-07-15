"""
Radar Target Simulation Module

This module provides realistic simulation of radar echoes including:
- Range-dependent signal attenuation 
- Complex Gaussian noise modeling
- Multiple target scenarios
"""

import numpy as np
from typing import List, Tuple, Optional, Union


def simulate_echoes(pulse: np.ndarray,
                   sample_rate: float,
                   targets: Union[List[float], List[Tuple[float, float]]],
                   noise_std: float = 0.0) -> Tuple[np.ndarray, np.ndarray]:
    """
    Simulate radar echoes from multiple targets with realistic effects.
    
    This function models the complete radar channel including propagation
    delays, path loss, and additive noise. 
    
    Parameters
    ----------
    pulse : np.ndarray
        Transmitted radar pulse (complex baseband signal).
    sample_rate : float
        Sampling frequency in Hz.
    targets : list
        List of target ranges in meters.
    noise_std : float, optional
        Standard deviation of complex Gaussian noise. Default is 0.0.
    Returns
    -------
    tuple
        (received_signal, time_axis) where received_signal is the complex
        baseband signal containing all echoes and noise.
        
    Notes
    -----
    The received power follows the radar equation:
        Pr = Pt * G^2 * λ^2 * σ / ((4π)^3 * R^4)
    
    For simplicity, we model this as amplitude ∝ 1/R^2.
    """
    c = 3e8  # Speed of light
    
    target_ranges = [t for t in targets]
    
    # Calculate required signal duration
    max_distance = max(target_ranges)
    max_delay = 2 * max_distance / c  # Round-trip time
    pulse_duration = len(pulse) / sample_rate
    
    # Add buffer for visualization
    total_duration = 5e-6 + max_delay + pulse_duration
    total_samples = int(total_duration * sample_rate)
    
    # Initialize received signal
    received_signal = np.zeros(total_samples, dtype=complex)
    
    # Add echo from each target
    for range_m in target_ranges:
        # Calculate round-trip delay
        delay = 2 * range_m / c
        delay_samples = int(delay * sample_rate)
        
        # Skip if echo would exceed buffer
        if delay_samples + len(pulse) > total_samples:
            continue
        
        # Calculate signal attenuation (simplified radar equation)
        # Amplitude proportional to 1/R^2 (power proportional to 1/R^4)
        amplitude = 1 / range_m**2
        
        # Add delayed and attenuated echo
        received_signal[delay_samples:delay_samples + len(pulse)] += amplitude * pulse

    
    # Add thermal noise
    if noise_std > 0:
        received_signal = add_complex_noise(received_signal, noise_std)
    
    # Generate time axis
    t = np.arange(len(received_signal)) / sample_rate
    
    return received_signal, t


def add_complex_noise(signal: np.ndarray, noise_std: float) -> np.ndarray:
    """
    Add complex Gaussian noise to a signal.
    
    For complex signals, noise is added to both I and Q channels
    independently with variance noise_std^2/2 each
    
    Parameters
    ----------
    signal : np.ndarray
        Input signal (complex or real).
    noise_std : float
        Standard deviation of the complex noise.
    
    Returns
    -------
    np.ndarray
        Signal with added noise.
    """
    # For complex Gaussian noise: σ_I = σ_Q = σ_total / √2
    sigma_component = noise_std / np.sqrt(2)
    
    # Generate independent Gaussian noise for I and Q
    noise_i = np.random.normal(0, sigma_component, size=signal.shape)
    noise_q = np.random.normal(0, sigma_component, size=signal.shape)
    
    # Combine into complex noise
    noise = noise_i + 1j * noise_q
    
    return signal + noise



def create_target_scenario(scenario_type: str = "simple") -> List[Tuple[float, float]]:
    """
    Create predefined target scenarios for testing.
    
    Parameters
    ----------
    scenario_type : str
        Type of scenario: "simple", "dense", "extended", "challenging"
    
    Returns
    -------
    list
        List of targets ranges (ints) defining the target scenario.
    """
    scenarios = {
        "simple": [
            1600,   
            2500,   
            4000,   
        ],
        "dense": [   
            1000,
            1080,
            1160,
            3500,
            3600,
            4500,
            4700,
        ],
        "extended": [
            2000,
            3000,
            4000,
            5000,
            6000,
            8000,
            9000,
        ]
    }
    
    return scenarios.get(scenario_type, scenarios["simple"])

