#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a 2 dimensional root finidng problem.
Parameters taken from GNU GSL Manual
"""

from sympy import exp as e

from symneqsys import SimpleNEQSys, NLRFP
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


def main():
    """
    Solve the example system using NLEQ2 fortran routine.
    """

    sys = ExampleSys()
    problem = NLRFP(sys, {'A': 100}, guess={'x0': 1.0, 'x1': 1.0},
                    solver=GSL_Solver())#SciPy_Solver())

    success = problem.solve(itermax=100)

    if success:
        print("Successfully found a root at x0={}, x1={}".format(
            problem.solution[sys['x0']], problem.solution[sys['x1']]))
    else:
        print("Root-finding unsuccessful.")


if __name__ == '__main__':
    main()
