class TransmissionSimulation(object):
    """docstring for TransmissionSimulation"""
    def __init__(self, original_wave, c1, c2):
        self.original_wave = original_wave
        self.c1 = c1
        self.c2 = c2

        self.speed_ratio = c1/c2
        self.alpha = (self.speed_ratio - 1.0)/(self.speed_ratio + 1.0)
        self.beta = 2.0*self.speed_ratio/(self.speed_ratio + 1.0)

    def total_wave(self, x, t):
        if x < 0.0:
            return self.original_wave(x,t) + self.alpha * self.original_wave(-x, t)
        else:
            return self.beta * self.original_wave(self.speed_ratio * x, t)
        