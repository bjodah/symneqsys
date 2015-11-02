#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a 2 dimensional root finidng problem (Rosenbrock).
Parameters taken from GNU GSL Manual
"""

from symneqsys import SimpleNEQSys, Problem
from symneqsys.gsl import GSL_Solver


class RosenbrockSys(SimpleNEQSys):
    param_tokens = 'a b'
    var_tokens = 'x0 x1'

    @property
    def exprs(self):
        x0, x1, a, b = [self[token] for token
                        in ('x0', 'x1', 'a', 'b')]
        return [a*(1-x0),
                b*(x1-x0**2)]


def main(Sys, solver_type):
    """
    Solve the example system using NLEQ2 fortran routine.
    """

    sys = Sys()
    solver = GSL_Solver(save_temp=True, tempdir='./build/rosenbrock')
    solver.abstol = 1e-8
    problem = Problem(sys, {'a': 1, 'b': 10},
                      guess={'x0': -10, 'x1': -5},
                      solver=solver)

    success = problem.solve(itermax=100, solver_type=solver_type)

    if success:
        print("Successfully found a root at x0={}, x1={}, using {}".format(
            problem.solution[sys['x0']], problem.solution[sys['x1']],
            solver_type))
    else:
        print("Root-finding unsuccessful.")
    print('Full numerical info:', problem.solver.num_result)


if __name__ == '__main__':
    for solver_type in ('newton', 'gnewton', 'hybridj', 'hybridsj'):
        print('='*30)
        print(solver_type)
        print('-'*30)
        main(RosenbrockSys, solver_type)
