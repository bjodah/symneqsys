#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a non linear least square fit from
overdetermined non-linear system. I.e. there are
more data point (deviance relations) than parameters
to be fitted

Transcribed from GNU Scientific Library Reference Manual v1.15 p. 419

"""

import sympy
import numpy as np

from symneqsys import SimpleNEQSys, Problem
from symneqsys.gsl import GSL_Solver

class ExpbSys(SimpleNEQSys):
    """
    Fits data to exponential curve
    """

    # TODO: Add support for loop construction in codeexport.
    param_tokens = 'x[i] y[i] s[i]'
    var_tokens = 'A l b'

    @property
    def exprs(self):
        f = lambda x: self['A']*sympy.exp(-self['l']*x)+self['b']
        x,y,s = self['x','y','s']
        return [(f(x) - y)/s]


def main(Sys):
    sys = Sys()
    x = np.linspace(0,39,40)
    y = 1.0*5*np.exp(-0.1*x)+np.random.normal(scale=0.1,size=x.size)
    problem = Problem(sys, {'x[i]': x, 'y[i]': y},
                      solver=GSL_Solver(save_temp=True, tempdir='./build/expfit'))
    success = problem.solve()
    if success:
        print("Success:")
        print(problem.solution)
    else:
        print("Root-finding unsuccessful.")
    print('='*30)
    print('Full numerical info:', problem.solver.num_result)


if __name__ == '__main__':
    main(ExpbSys)
