
import numpy as np
cimport numpy as cnp

cdef extern c_solve(double * x, double * tol, int * info)

def solve(double [:] x0, double [:] params, double atol,
          str solver_type = 'gnewton', int itermax=100):
    c_solve(&x[0], params[0], &tol, &info)
