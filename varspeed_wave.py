import math
import numpy as np

class WaveSimulation(object):
    """docstring for WaveSimulation"""
    def __init__(self, wave_init, wave_deriv_init, wave_speed_func,
        delta_x, delta_t, x_lower, x_upper):
        self.wave_init = wave_init
        self.wave_deriv_init = wave_deriv_init
        self.wave_speed_func = wave_speed_func

        self.t = 0
        self.delta_x = delta_x
        self.delta_t = delta_t

        self.x_lower = x_lower
        self.x_upper = x_upper

        self.last_index = int((x_upper - x_lower)/delta_x)
        self.wave = np.array([self.wave_init(x_lower + i*delta_x) for i in range(self.last_index)])
        self.wave_deriv = np.array([self.wave_deriv_init(x_lower + i*delta_x) for i in range(self.last_index)])

        self._updated_wave = np.zeros(self.last_index)

    def index_to_x(self, space_index):
        return self.x_lower + space_index*self.delta_x

    def calc_wave_second_deriv(self, space_index):
        x_val = self.index_to_x(space_index)
        centre_val = self.wave[space_index]
        left_val = 0
        if space_index > 0:
            left_val = self.wave[space_index - 1]

        right_val = 0
        if space_index < self.last_index - 1:
            right_val = self.wave[space_index + 1]

        return ((self.wave_speed_func(x_val + self.delta_x/2))**2 * (right_val - centre_val) 
            - (self.wave_speed_func(x_val - self.delta_x/2))**2 * (centre_val - left_val)
            )/(self.delta_x**2)

    def _update_wave_deriv(self):
        #TODO: matrix multiplcation/vectorize
        for space_index in range(len(self.wave_deriv)):
            self.wave_deriv[space_index] += self.delta_t * self.calc_wave_second_deriv(space_index)

    def _update_wave(self):
        #TODO: matrix multiplcation/vectorize
        for space_index in range(len(self.wave)):
            self.wave[space_index] += self.delta_t * self.wave_deriv[space_index]

    def iterate(self):
        self._update_wave()
        self._update_wave_deriv()
        self.t += self.delta_t

    def calc_max_wave_speed(self):
        sample = self.x_lower
        curr_max = 0

        while sample <= self.x_upper:
            curr_max = max(self.wave_speed_func(sample), curr_max)
            sample += self.delta_x

        return curr_max

    # gives an upper bound on the error after time t to the best possible solution with this fixed delta_x
    # Note: this is currently very impractical and ridiculously too conservative (upper bound is astronomical)
    def calc_error_bound(self, t):
        n = int(t/self.delta_t)
        operator_norm_bound = 4*self.calc_max_wave_speed()**2 / (self.delta_x)**2

        return (1 + self.delta_t * operator_norm_bound)**n - math.exp(t*operator_norm_bound)



        