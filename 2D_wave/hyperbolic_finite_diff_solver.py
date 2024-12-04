import math
import numpy as np

def create_zero_table(width, height, dim_entry):
    [[np.array(dim_entry*[0]) for _ in range(height)] for _ in range(width)]

# following Fritz John book and notation there for matrix valued functions A_1,A_2, B and 
# vector valued functions w, v.
class HyperbolicFiniteDifferenceSolver(object):
    def __init__(self, A_1, A_2, B, w,
                    delta_t, delta_x, x_lower, x_upper, y_lower, y_upper):

        self.t = 0
        self.delta_x = delta_x
        self.delta_t = delta_t
        self.dim = 2 #TODO: can generalize

        self.x_lower = x_lower
        self.x_upper = x_upper
        self.last_index_x = int((x_upper - x_lower)/delta_x)

        self.y_lower = y_lower
        self.y_upper = y_upper
        self.last_index_y = int((y_upper - y_lower)/delta_x)

        self.A_1 = A_1
        self.A_2 = A_2
        self.B = B
        self.w = w

        self.v_table = create_zero_table(last_index_x, last_index_y, self.dim)

    def index_to_point(self, index):
        return np.array([x_lower + index[0]*self.delta_x, y_lower + index[1]*self.delta_x])

    def _calc_a_j_term(self, index):
        point = self.index_to_point(index)
        right_index = (index[0] + self.delta_x, index[1])
        up_index = (index[0], index[1] + self.delta_x)

        result = (1.0/(2*self.dim))*self.v_table[right_index[0]][right_index[1]]
        result += (1.0/(2*self.dim))*self.v_table[up_index[0]][up_index[1]]
        result += -(self.delta_t/(2*self.delta_x)) * self.A_1(point, self.v_table[right_index[0]][right_index[1]])
        result += -(self.delta_t/(2*self.delta_x)) * self.A_2(point, self.v_table[up_index[0]][up_index[1]])

        return result

    def _calc_b_j_term(self, index):
        point = self.index_to_point(index)
        left_index = (index[0] - self.delta_x, index[1])
        down_index = (index[0], index[1] - self.delta_x)

        result = (1.0/(2*self.dim))*self.v_table[left_index[0]][left_index[1]]
        result += (1.0/(2*self.dim))*self.v_table[down_index[0]][down_index[1]]
        result += (self.delta_t/(2*self.delta_x)) * self.A_1(point, self.v_table[left_index[0]][left_index[1]])
        result += (self.delta_t/(2*self.delta_x)) * self.A_2(point, self.v_table[down_index[0]][down_index[1]])

        return result

    def calc_B_term(self, index):
        point = self.index_to_point(index)
        return self.B(point, self.v_table[index[0]][index[1]])

    def calc_w_term(self, index):
        point = self.index_to_point(index)
        return self.w(point, self.t)

    def update(self):
        updated_v_table = create_zero_table(last_index_x, last_index_y, self.dim)
        #TODO: need to handle boundary values better
        for x_index in range(1,self.last_index_x - 1):
            for y_index in range(1,self.last_index_y - 1):
                new_val = self._calc_a_j_term((x_index, y_index))
                new_val += self._calc_b_j_term((x_index, y_index))
                new_val += -self.delta_t * self.calc_B_term((x_index, y_index))
                new_val += self.delta_t * self.calc_w_term((x_index, y_index))


                updated_v_table[x_index][y_index] = new_val

        self.v_table = updated_v_table
        self.t += self.delta_t

