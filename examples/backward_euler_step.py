#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a 2 dimensional root finidng problem (Powell).
Parameters taken from GNU GSL Manual
"""

from math import sin, cos

from symneqsys import SimpleNEQSys, Problem
from symneqsys.gsl import GSL_Solver

y0, y1 = 0.0, 1.0

class EulerBackwardStep(SimpleNEQSys):

    param_tokens = 'h'
    var_tokens = 'x0 x1'

    @property
    def exprs(self):
        x0, x1, h = self['x0'], self['x1'], self['h']
        y0, y1 = 0, 1
        return [x1*h-x0+y0,
                -x0*h-x1+y1]

def main(Sys, solver_type, logger=None):
    """
    Solves a backward step of a newton iteration
    """
    sys = Sys()
    problem = Problem(
        sys, params={'h':0.02}, guess={'x0': 0.02, 'x1': 1.0}, solver=GSL_Solver(
            save_temp=True, tempdir='./build/backward_euler_step', logger=logger))

    success = problem.solve(itermax=100, solver_type=solver_type, abstol=1e-12)

    if success:
        print("Successfully found a root at x0={}, x1={}, using {}".format(
            problem.solution[sys['x0']], problem.solution[sys['x1']],
            solver_type))
        x0, x1 = problem.solution[sys['x0']], problem.solution[sys['x1']]
    else:
        print("Root-finding unsuccessful.")
    print('Full numerical info:', problem.solver.num_result)

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = None #logging.getLogger(__file__)
    for solver_type in ('newton', 'gnewton', 'hybridj', 'hybridsj'):
        print('='*30)
        print(solver_type)
        print('-'*30)
        main(EulerBackwardStep, solver_type, logger)
