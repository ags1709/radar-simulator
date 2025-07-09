# Mini Radar Simulation System

This project simulates a basic radar system that emits pulses, receives echoes from simulated targets, and processes the signal to detect object distances. The simulation includes noise modeling and visual output.

## Features
- Pulse generation
- Target reflection modeling
- Additive noise
- Signal processing (Matched filter + simple peak detection)
- Visualization of detections




#### Project notes:
Distance calculations were off by roughly ~150m due to using the center of the matched filtered pulses for the distance calculations instead of the beginning.
After taking that into consideration calculated distances are within 2 meters of the real distances.



