from transmission_simulation import *
from plotter import *

import math

c1 = 5.0
c2 = 20.0

def bump_func(x,t):
    if -3*math.pi < x - c1 * t < -1*math.pi:
        return math.cos(x - c1*t) + 1
    else:
        return 0.0

def sudden_sine(x,t):
    if x - c1 * t < -1*math.pi:
        return math.cos(x - c1*t) + 1
    else:
        return 0.0

simulation = TransmissionSimulation(sudden_sine, c1, c2)

plot_spacetime_function(lambda x,t: simulation.total_wave(x,t), x_delta = 0.01,
                    colour_rule = sign_colour_rule)