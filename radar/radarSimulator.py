import numpy as np, time
from radar.simulator import generate_lfm_pulse
from radar.targets import simulate_echoes
from radar.signalProcessing import matched_filter, ca_cfar_detector

class RadarSimulator:
    """Main radar simulation class with configurable parameters."""
    
    def __init__(self, sample_rate=100e6, bandwidth=20e6, pulse_duration=10e-6, n_pulses=128, prf=5e3):
        self.sample_rate = sample_rate
        self.bandwidth = bandwidth
        self.pulse_duration = pulse_duration
        self.n_pulses = n_pulses
        self.prf = prf
        self.pri = 1.0 / prf
        self.c = 3e8  # Speed of light
        
        # Performance metrics
        self.range_resolution = self.c / (2 * self.bandwidth)
        print(f"Theoretical range resolution: {self.range_resolution:.2f} m")
        self.unambiguous_range = self.c * self.pri / 2
        print(f"PRF                         : {self.prf/1e3:.1f} kHz")
        print(f"PRI                         : {self.pri*1e6:.1f} µs")
        print(f"Max unambiguous range       : {self.unambiguous_range/1e3:.2f} km")
        
    def generate_pulse(self, window='hanning'):
        """Generate LFM chirp pulse."""
        pulse, t_pulse = generate_lfm_pulse(
            start_freq=-self.bandwidth/2,
            bandwidth=self.bandwidth,
            duration=self.pulse_duration,
            sample_rate=self.sample_rate,
            window=window
        )
        return pulse, t_pulse
    
    def process_single_pulse(self, pulse, targets, noise_std=3e-7):
        """Transmit → receive → compress one pulse whose record length == PRI."""
        pri_samples = int(round(self.pri * self.sample_rate))

        received_signal, _ = simulate_echoes(
            pulse, self.sample_rate, targets, noise_std=noise_std
        )

        # Force exactly one PRI of data (pad or truncate)
        if len(received_signal) < pri_samples:
            received_signal = np.pad(received_signal,
                                     (0, pri_samples - len(received_signal)))
        else:
            received_signal = received_signal[:pri_samples]

        mf_output = matched_filter(received_signal, pulse)
        t = np.arange(pri_samples) / self.sample_rate
        return received_signal, mf_output, t

    
    def coherent_integration(self, pulse, targets, noise_std=3e-7):
        # """Perform coherent integration over multiple pulses."""
        """Transmit *n_pulses* back-to-back at the chosen PRF and coherently add the matched-filter outputs."""
        print(f"\nPerforming coherent integration over {self.n_pulses} pulses...")
        
        range_lines = []
        start_time = time.time()
        pri_samples = int(round(self.pri * self.sample_rate))
        
        for i in range(self.n_pulses):
            echoes, _ = simulate_echoes(pulse, self.sample_rate, targets, noise_std=noise_std)

            if len(echoes) < pri_samples:                # pad / truncate
                echoes = np.pad(echoes, (0, pri_samples - len(echoes)))
            else:
                echoes = echoes[:pri_samples]

            range_lines.append(matched_filter(echoes, pulse))
            
            # Progress indicator
            if (i + 1) % 32 == 0:
                print(f"  Processed {i + 1}/{self.n_pulses} pulses...")
        
        # Stack and integrate
        rd_matrix = np.vstack(range_lines)
        integrated = np.sum(rd_matrix, axis=0)
        
        processing_time = time.time() - start_time
        print(f"Processing completed in {processing_time:.2f} seconds")
        
        return integrated, rd_matrix
    
    def detect_targets(self, signal, echo_time, pulse_length, cfar_params=None):
        """Detect targets using CA-CFAR."""
        if cfar_params is None:
            cfar_params = {
                'num_train': 35,
                'num_guard': 5,
                'pfa': 8e-3,
                'peak_guard': 1
            }
        
        # Detect peaks
        peaks = ca_cfar_detector(signal, **cfar_params)
        
        # Correct for matched filter delay
        correction_samples = pulse_length // 2
        corrected_peaks = peaks - correction_samples
        corrected_peaks = corrected_peaks[corrected_peaks >= 0]
        
        # Convert to distance
        peak_times = corrected_peaks / self.sample_rate
        distances = (peak_times * self.c) / 2
        
        return peaks, distances
    
    def analyze_performance(self, true_targets, detected_distances):
        """Analyze detection performance."""
        print("\n" + "="*50)
        print("PERFORMANCE ANALYSIS")
        print("="*50)
        
        # Convert to numpy arrays for easier manipulation
        true_targets = np.array(true_targets)
        detected_distances = np.array(detected_distances)
        
        print(f"\nTrue target ranges (m): {true_targets}")
        print(f"Detected ranges (m): {detected_distances}")
        
        # Match detections to true targets
        if len(detected_distances) == len(true_targets):
            errors = detected_distances - true_targets
            print(f"\nRange errors (m): {errors}")
            print(f"Mean error: {np.mean(errors)} m")
            print(f"RMS error: {np.sqrt(np.mean(errors**2))} m")
            
        else:
            print(f"\nWarning: Detected {len(detected_distances)} targets, "
                  f"expected {len(true_targets)}")
