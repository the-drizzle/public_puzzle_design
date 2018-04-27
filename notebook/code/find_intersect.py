import numpy as np
from sympy import symbols, sqrt, solvers

class FindParabolaDimension(object):
    def __init__(self, edge_length):
        self.R = edge_length

    def solve_ab(self, a_init=1e-5, step_size=1e-3):
        a, b, x, d, R = symbols('a, b, x, d, R')
        b = (6 * sqrt(2) * R - 17 * a * R**2) / 36

        f0 = a * ((a * (x**2 + R**2/4) + b)**2 + R**2/4) + b - x
        f1 = a*x**2 -x + b - sqrt(2)*R/2

        def root_fn(fn, a_):
            res = []
            roots = solvers.solve(fn.subs(R, self.R).subs(a, a_), x)

            for root in roots:
                try:
                    i = np.float64(root)
                    if -np.sqrt(2) * self.R/2 <= i <= np.sqrt(2) * self.R/2:
                        res += [i]

                except:
                    pass
            
            return res

        def num_est(val):
            # horribly slow...
            d_ = np.zeros(5)
            for i in range(5):
                temp0 = np.float64(root_fn(f0, a_ + (i-2)*h)[0])
                temp1 = np.float64(root_fn(f1, a_ + (i-2)*h)[0])
                
                d_[i] = np.sqrt(2) * (temp0 + temp1) + self.R/2
                
            return d_[2], (-d_[4] + 8*d_[3] - 8*d_[1] + d_[0]) / (12*h)

        delta = 1
        a_ = a_init
        h = step_size
    
        while np.abs(delta) > 1e-9:
            delta, delta_ = num_est(a_)
            a_ = a_ - delta / delta_
            b_ = np.float64(b.subs(R, self.R).subs(a, a_))

        return a_, b_
