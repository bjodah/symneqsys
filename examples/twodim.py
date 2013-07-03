#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a 2 dimensional root finidng problem (Powell).
Parameters taken from GNU GSL Manual
"""

from sympy import exp as e

from symneqsys import SimpleNEQSys, Problem
#from symneqsys.solver import SciPy_Solver
from symneqsys.gsl import GSL_Solver

class ExampleSys(SimpleNEQSys):

    param_tokens = 'A'
    var_tokens = 'x0 x1'

    @property
    def exprs(self):
        x0, x1, A = self['x0'], self['x1'], self['A']
        return [A*x0*x1-1,
                (e(-x0)+e(-x1)-(1+1/A))]


def main(solver_type):
    """
    Solve the example system using NLEQ2 fortran routine.
    """

    sys = ExampleSys()
    problem = Problem(sys, {'A': 1e4}, guess={'x0': 0.5, 'x1': 1.5},
                    solver=GSL_Solver(save_temp=True, tempdir='./build/powell'))#SciPy_Solver())

    success = problem.solve(itermax=100, solver_type=solver_type)

    if success:
        print("Successfully found a root at x0={}, x1={}, using {}".format(
            problem.solution[sys['x0']], problem.solution[sys['x1']],
            solver_type))
        print('Full numerical info:', problem.solver.num_result)
    else:
        print("Root-finding unsuccessful.")


if __name__ == '__main__':
    main('newton')
    main('gnewton')
    main('hybridj') # segfaults...
    main('hybridsj')
