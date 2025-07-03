from radar.simulator import generate_pulse
from visualizations.plotResults import plotPulse

pulse, time = generate_pulse()

plotPulse(pulse, time)
