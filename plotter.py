import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import math
import time

def plot_spacetime_function(func, x_delta = 0.1, t_delta = 0.1, 
    x_lims = [-30,10], y_lims = [-5,5], init_t = 0.0,
    colour_rule = None):
        t = init_t
        x_vals = [x_lims[0] + i*x_delta for i in range(int((x_lims[1] - x_lims[0])/x_delta))]

        ax = plt.axes()
        fig = plt.figure()
        fig.show()


        while True:
            plt.clf()
            y_vals = [func(x, t) for x in x_vals]
            colour = 'red'
            if colour_rule is not None:
                colour = [colour_rule(x,t) for x in x_vals]
            plt.scatter(x_vals, y_vals,
                s = 1,
                color = colour)
            
            plt.axis([x_lims[0], x_lims[1], y_lims[0], y_lims[1]])
            fig.canvas.draw()
            t += t_delta
            time.sleep(t_delta)

def sign_colour_rule(x,t):
    if (x<0):
        return 'red'
    else:
        return 'blue'
