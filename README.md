# Mini Radar Simulation System

This project simulates a basic radar system that emits pulses, receives echoes from simulated targets, and processes the signal to detect object distances. The simulation includes noise modeling and visual output.

## Features
- Pulse generation
- Target reflection modeling
- Additive noise
- Signal processing (Matched filter + simple peak detection)
- Accurate range calculations
- Visualization of detections




## Theory
Linear Frequency-Modulated chirp (Very good range resolution)
Range
Range resolution (ΔR = c / (2B))
SNR
PRF -> max range
Tradeoff between SNR and range resolution
Matched filter
Velocity /+ max unambigious velocity


## TO-DO
More realistic transmit signals, chirp or whatever it is real radars do
Simulate moving targets and calculate velocity using the doppler effect
Improved visualizations +/ dashboard?
visualize the received signal as more and more pulses are added together
Optimize some parts using c/c++
Do 2d/3d simulation instead of 1d?
Radar cross section
Complex gaussian noise?


## Project notes:
Distance calculations were off by roughly ~150m due to using the center of the matched filtered pulses for the distance calculations instead of the beginning.
After taking that into consideration calculated distances are within 2 meters of the real distances.

radar range: R = c * t / 2


