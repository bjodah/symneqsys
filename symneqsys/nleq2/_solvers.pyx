# -*- coding: utf-8 -*-

# Cython wrapper of solvers.f90 (which is generated from solvers_template.f90)

import numpy as np
cimport numpy as cnp

def solve(double [::1] x0, double [::1] params, double atol,
          str solver_type = 'gnewton', int itermax=100):
    return None
