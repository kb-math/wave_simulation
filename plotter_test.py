from plotter import *

import math

def sine_wave(x,t):
    return math.sin(x - t)

test_func = sine_wave

plot_spacetime_function(test_func, x_delta = 0.1)
