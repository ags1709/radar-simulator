from .simulator import generate_pulse, generate_lfm_pulse
from .targets import simulate_echoes
from .signalProcessing import (
    matched_filter,
    ca_cfar_detector,
    # estimate_noise_floor,
    # calculate_snr,
    # pulse_compression_gain
)

__all__ = [
    "generate_pulse",
    "generate_lfm_pulse", 
    "simulate_echoes",
    "matched_filter",
    "ca_cfar_detector",
    "ca_cfar_peak",
    "go_cfar_detector",
    "so_cfar_detector",
    "estimate_noise_floor",
    "calculate_snr",
    "pulse_compression_gain"
]