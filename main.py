import argparse

from radar.targets import create_target_scenario
from visualizations.plotResults import (
    plot_complex_pulse,
    plot_comprehensive_results,
)
from radar.radarSimulator import RadarSimulator


# ----------------------------------------------------------------------
# CLI handling
# ----------------------------------------------------------------------
def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Radar signal‑processing pipeline"
    )
    parser.add_argument(
        "-s",
        "--scenario",
        choices=["simple", "dense", "extended"],
        default="dense",
        help="Target distribution to simulate",
    )
    parser.add_argument(
        "--show-pulse",
        action="store_true",
        help="Plot the transmitted LFM chirp",
    )
    return parser.parse_args()


# ----------------------------------------------------------------------
# Main simulation driver
# ----------------------------------------------------------------------
def main() -> None:
    args = _parse_args()

    print("RADAR SIGNAL PROCESSING SIMULATOR")
    print("=" * 50)

    # ------------------------------------------------------------------
    # 1. Instantiate simulator
    # ------------------------------------------------------------------
    radar = RadarSimulator(
        sample_rate=100e6, # 100 MHz
        bandwidth=20e6, # 20 MHz
        pulse_duration=10e-6, # 10 μs
        n_pulses=128,
        prf=5e3, # 5 KHz
    )

    # ------------------------------------------------------------------
    # 2. Create targets according to the chosen scenario
    # ------------------------------------------------------------------
    targets = create_target_scenario(args.scenario)
    print(f"\nTarget Scenario: {args.scenario!r}")
    print(f"Simulating {len(targets)} targets at ranges: {targets} m")

    # ------------------------------------------------------------------
    # 3. Generate one transmit pulse
    # ------------------------------------------------------------------
    pulse, t_pulse = radar.generate_pulse(window="hanning")

    if args.show_pulse:
        plot_complex_pulse(
            pulse=pulse,
            t=t_pulse,
            title="Transmitted LFM Chirp (20 MHz bandwidth, 10 µs duration)",
        )

    # ------------------------------------------------------------------
    # 4. Run the processing chain on a single pulse
    # ------------------------------------------------------------------
    print("\nProcessing single pulse…")
    received_signal, mf_single, echo_time = radar.process_single_pulse(
        pulse, targets, noise_std=3e-7
    )

    # ------------------------------------------------------------------
    # 5. Coherently integrate many pulses
    # ------------------------------------------------------------------
    integrated, _ = radar.coherent_integration(pulse, targets, noise_std=3e-7)

    # ------------------------------------------------------------------
    # 6. CA‑CFAR detection and performance analysis
    # ------------------------------------------------------------------
    peaks, distances = radar.detect_targets(integrated, echo_time, len(pulse))
    radar.analyze_performance(targets, distances)

    # ------------------------------------------------------------------
    # 7. Visualisation
    # ------------------------------------------------------------------
    plot_comprehensive_results(
        received_signal=received_signal,
        mf_single=mf_single,
        integrated=integrated,
        n_pulses=radar.n_pulses,
        echo_time=echo_time,
        peaks=peaks,
        distances=distances,
        targets=targets,
    )

    print("\n" + "=" * 50)
    print("SIMULATION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
