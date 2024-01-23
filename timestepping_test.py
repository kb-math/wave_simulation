from varspeed_wave import *

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import time

x_lower = -20
x_upper = 20
y_lower = -5
y_upper = 5
delta_x = 0.1
delta_t = 0.1

def wave_init(x):
    if -3*math.pi < x < - math.pi:
        return math.cos(x) + 1
    else:
        return 0

def wave_deriv_init(x):
    if -3*math.pi < x < - math.pi:
        return math.sin(x)
    else:
        return 0

def wave_speed_func(x):
    if x < 0.0:
        return 1.0
    elif 0.0<=x<5.0:
        return 0.5
    else:
        return 1.0

wave_sim = WaveSimulation(wave_init, wave_deriv_init, wave_speed_func,
        delta_x, delta_t, x_lower, x_upper)

ax = plt.axes()
fig = plt.figure()
fig.show()

x_vals = [wave_sim.x_lower + i * delta_x for i in range(wave_sim.last_index)]
speed_vals = [wave_sim.wave_speed_func(x) for x in x_vals]
print (wave_sim.calc_max_wave_speed())

time_max = 0.5
for i in range(2000):
    plt.clf()
    y_vals = wave_sim.wave
    colour = 'red'
    plt.scatter(x_vals, y_vals,
                s=1,
                c = speed_vals)

    plt.axis([x_lower, x_upper, y_lower, y_upper])
    fig.canvas.draw()

    wave_sim.iterate()
    plt.pause(delta_t)