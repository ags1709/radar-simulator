import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
import seaborn as sns

sns.set_theme(style="darkgrid")
sns.set_palette("husl")


def plot_pulse(pulse, time, title):
    """Plot real-valued pulse with enhanced formatting."""
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.plot(time * 1e6, pulse, linewidth=2)
    ax.set_xlabel("Time (μs)", fontsize=12)
    ax.set_ylabel("Amplitude", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Add pulse duration annotation
    duration = (time[-1] - time[0]) * 1e6
    ax.text(0.02, 0.95, f'Duration: {duration:.1f} μs', 
            transform=ax.transAxes, 
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()



def plot_complex_pulse(pulse, t, title="Complex Pulse"):
    """Comprehensive complex pulse visualization."""
    fig = plt.figure(figsize=(12, 10))
    fig.subplots_adjust(top=0.93, hspace=0.4, wspace=0.3)  # manually control spacing
    gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)
    
    # Time domain - I/Q components
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(t*1e6, np.real(pulse), label="In-phase (I)", linewidth=2)
    ax1.plot(t*1e6, np.imag(pulse), label="Quadrature (Q)", 
             linewidth=2, alpha=0.8)
    ax1.set_ylabel("Amplitude", fontsize=11)
    ax1.set_title(title + " - Time Domain", fontsize=12)
    ax1.legend(loc="upper right")
    ax1.grid(True, alpha=0.3)
    
    # Envelope
    ax2 = fig.add_subplot(gs[1, :])
    envelope = np.abs(pulse)
    ax2.plot(t*1e6, envelope, color='darkgreen', linewidth=2)
    ax2.fill_between(t*1e6, 0, envelope, alpha=0.3, color='darkgreen')
    ax2.set_ylabel("Magnitude", fontsize=11)
    ax2.set_title("Signal Envelope", fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Instantaneous frequency
    ax3 = fig.add_subplot(gs[2, :])
    phase = np.unwrap(np.angle(pulse))
    inst_freq = np.diff(phase) / (2*np.pi*np.diff(t))
    ax3.plot(t[1:]*1e6, inst_freq/1e6, color='darkred', linewidth=2)
    ax3.set_ylabel("Frequency (MHz)", fontsize=11)
    ax3.set_xlabel("Time (μs)", fontsize=11)
    ax3.set_title("Instantaneous Frequency", fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    plt.suptitle(f"LFM Chirp Analysis - Bandwidth: 20 MHz, Duration: 10 μs", 
                 fontsize=14, fontweight='bold')
    plt.show()

def calc_window_usec(echo_time, peaks, targets, safety_factor=1.1):
    """
    Decide where to stop the x-axis (in µs):
    • If peaks are available, use the last peak location.
    • Otherwise use the scripted furthest target range.
    Adds a small safety margin so the annotation boxes fit.
    """
    c = 3e8

    if len(peaks):                               # use detections if we have them
        t_stop = echo_time[peaks[-1]]            # seconds
    else:                                        # fall back to target list
        r_max  = max(targets)
        t_stop = 2 * r_max / c                   # first sample AFTER echo

    # Always include the transmit pulse itself
    t_stop = max(t_stop, echo_time[0] + 2e-5)    # at least 20 µs
    return t_stop * 1e6 * safety_factor          # → µs with margin


def plot_comprehensive_results(received_signal, mf_single, integrated, n_pulses, 
                             echo_time, peaks, distances, targets):
    """Create comprehensive multi-panel results visualization."""
    fig = plt.figure(figsize=(16, 12))
    fig.subplots_adjust(top=0.93, hspace=0.4, wspace=0.3)  # manually control spacing
    gs = GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.2)
    
    # 1. Raw received signal
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(echo_time*1e6, np.abs(received_signal), linewidth=1, alpha=0.8)
    ax1.set_xlabel("Time (μs)")
    ax1.set_ylabel("Amplitude")
    ax1.set_title("Raw Received Signal (Single Pulse)", fontweight='normal', fontsize=12)
    ax1.grid(True, alpha=0.3)
    
    # 2. Single pulse matched filter output
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(echo_time*1e6, np.abs(mf_single), linewidth=1.5, color='orange')
    ax2.set_xlabel("Time (μs)")
    ax2.set_ylabel("Amplitude")
    ax2.set_title("Matched Filter Output (Single Pulse)", fontweight='normal', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Integrated signal
    ax3 = fig.add_subplot(gs[1, :])
    ax3.plot(echo_time*1e6, np.abs(integrated), linewidth=2, 
             label='Integrated Signal', color='darkblue')
    ax3.set_xlabel("Time (μs)")
    ax3.set_ylabel("Amplitude")
    ax3.set_title(f"Coherently Integrated Signal ({n_pulses} Pulses)", fontweight='normal', fontsize=12)
    

    # 4. Integrated signal with detections
    ax4 = fig.add_subplot(gs[2, :])
    ax4.plot(echo_time*1e6, np.abs(integrated), linewidth=2, 
             label='Integrated Signal', color='darkblue')
    
    # Plot detected peaks
    ax4.plot(echo_time[peaks]*1e6, np.abs(integrated[peaks]), 'rx', 
             markersize=12, markeredgewidth=3, label='Detected Targets')
    
    # Add annotations
    peak_times_us = echo_time[peaks] * 1e6
    cluster_thresh = 3.0                      # μs → tweak if you like

    # 1) build clusters of neighbouring peaks
    clusters = [[0]]
    for idx in range(1, len(peaks)):
        if peak_times_us[idx] - peak_times_us[idx - 1] <= cluster_thresh:
            clusters[-1].append(idx)
        else:
            clusters.append([idx])
    # 2) label every cluster
    base_h_offsets = [-60, 5, 65, 50, 65, 90]  # repeats if >6/cluster
    for c_idx, cluster in enumerate(clusters):
        for j, p_idx in enumerate(cluster):
            peak   = peaks[p_idx]
            dist   = distances[p_idx]
            true_d = targets[p_idx]
            error  = dist - true_d

            h_off = base_h_offsets[j % len(base_h_offsets)]
            v_off = 20

            label = f'{dist:.1f}m\n(Δ={error:+.2f}m)'
            ax4.annotate(label,
                         xy=(echo_time[peak]*1e6, np.abs(integrated[peak])),
                         xytext=(h_off, v_off),
                         textcoords='offset points',
                         bbox=dict(boxstyle='round,pad=0.5',
                                   fc='yellow', alpha=0.8),
                         arrowprops=dict(arrowstyle='->',
                                         connectionstyle='arc3,rad=0.2',
                                         color="black"),
                         fontsize=10)
            
    
    ax4.set_xlabel("Time (μs)", fontsize=12)
    ax4.set_ylabel("Amplitude", fontsize=12)
    ax4.set_title("CA-CFAR Target Detection", 
                  fontsize=12, fontweight='normal')
    ax4.legend(loc='upper right')
    ax4.grid(True, alpha=0.3)

    x_stop = calc_window_usec(echo_time, peaks, targets)
    for ax in (ax1, ax2, ax3, ax4):
        ax.set_xlim(0, x_stop)
    
    # Add performance summary
    textstr = f'Targets Detected: {len(distances)}/{len(targets)}\n'
    if len(distances) == len(targets):
        errors = np.array(distances) - np.array(targets)
        textstr += f'Mean Error: {np.mean(errors):.2f} m\n'
        textstr += f'RMS Error: {np.sqrt(np.mean(errors**2)):.2f} m'
    
    ax4.text(0.02, 0.95, textstr, transform=ax4.transAxes, 
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
            fontsize=11)
    
    plt.suptitle("Radar Signal Processing Results", 
                fontsize=14, fontweight='bold')
    plt.show()
