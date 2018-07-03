#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a 2 dimensional root finidng problem (Langmuir).
Parameters taken from GNU GSL Manual
"""

from symneqsys import SimpleNEQSys, Problem
from symneqsys.gsl import GSL_Solver


class LangmuirSys(SimpleNEQSys):
    var_tokens = 'K alpha'

    def __init__(self, c0, data):
        self.c0 = c0
        self.param_tokens = ' '.join(['c'+str(i) for i in range(len(data))] +
                                     ['S'+str(i) for i in range(len(data))])
        self.data = data
        super(LangmuirSys, self).__init__()

    @property
    def exprs(self):
        K = self.known_symbs[0]
        alpha = self.known_symbs[1]
        c = self.known_symbs[2:2+len(self.data)]
        S = self.known_symbs[2+len(self.data):2+2*len(self.data)]
        return [K*c[i]*S[i]*alpha/(1+K*c[i])-c[i]-self.c0 for
                i, d in enumerate(self.data)]


def main(Sys, c0, data):
    """

    """
    sys = Sys(c0, data)
    solver = GSL_Solver(save_temp=True, tempdir='./build/langmuir')
    solver.abstol = 1e-6
    pt = sys.param_tokens.split()
    n = len(data)
    params = dict([(pt[i], d[0]) for i, d in enumerate(data)] +
                  [(pt[i+n], d[1]) for i, d in enumerate(data)])
    problem = Problem(sys, params, guess={'K': 1.0, 'alpha': 1e-5},
                      solver=solver)

    success = problem.solve()

    if success:
        print("Successfully found a root at x0={}, x1={}, using {}".format(
            problem.solution[sys['K']], problem.solution[sys['alpha']]))
    else:
        print("Root-finding unsuccessful.")
    print('Full numerical info:', problem.solver.num_result)


if __name__ == '__main__':
    print('='*30)
    print('Ru(bipy)3')
    main(LangmuirSys, 1.68e-5, [(1.68e-5, 0), (1.62e-5, 1.665e-4),
                                (1.46e-5, 3.49e-4)])
    print('-'*30)
    print('MB')
    main(LangmuirSys, 5.4e-6, [(5.4e-6, 0), (3.34e-6, 1.875e-4),
                               (3.51e-6, 3.445e-4), (2.2e-6, 6.99e-4)])
