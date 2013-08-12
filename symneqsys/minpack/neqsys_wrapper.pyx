# MINPACK wrapper for symneqsys

import time
import numpy as np
cimport numpy as cnp

from symneqsys.codeexport import Result

cdef extern void lm_solve(double * x, double * tol, int * info)

cdef extern void func(
    int * m, int * n, double * x, double * f, double * j, int * ldj, int * iflag
)

cdef extern void get_nfev(int * nfev)
cdef extern void get_njev(int * njev)
cdef extern void get_ne(int * ne_)
cdef extern void get_nx(int * nx_)

def solve(double [:] x0, double [:] params, double atol,
          str solver_type = 'lm', int itermax=100):
    """
    Solve using Levenberg-Marquardt algorithm
    """
    cdef double[:] x0_arr = x0.copy() # or np.ascontiguousarray ?
    cdef double[:] params_arr = params.copy() # or np.ascontiguousarray ?
    cdef cnp.ndarray[cnp.float64_t, ndim=1] x_and_param = \
        np.empty(x0.shape[0]+params.shape[0])
    cdef int nfev, njev, status

    start = time.time()
    lm_solve(&x_and_param[0], &atol, &status)
    end = time.time()
    get_nfev(&nfev)
    get_njev(&njev)

    return Result({
        'x': x0_arr,
        'success': status == 0,
        'status': status,
        'message': 'See lmder1.f for status meaning',
        'fun': residuals(x0_arr, params_arr),
        'jac': jac(x0_arr, params_arr),
        'nfev': nfev,
        'njev': njev,
        #'nit': iter_,
        #'allvecs': intermediate.reshape((itermax, x0.shape[0]))[:iter_+1,:],
        'walltime': end-start,# only C-call, excluding compilation
    })


def residuals(double [:] x, double [:] params):
    cdef cnp.ndarray[cnp.float64_t, ndim=1] x_arr = np.concatenate((x[::1], params[::1]))
    cdef int m = -1 # number of equations
    cdef int n = -1 # number of variables
    get_ne(&m)
    get_nx(&n)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] fvec = \
        np.empty(m)
    cdef cnp.ndarray[cnp.float64_t, ndim=2, mode='fortran'] fjac = \
        np.empty((m,n), order='F')
    cdef int ldj = n # leading dimensino of Jacobian matrix
    cdef int iflag = 1 # Calculate functions at x
    get_ne(&m)
    get_nx(&n)
    ldj = n
    func(&m, &n, &x_arr[0], &fvec[0], &fjac[0,0], &ldj, &iflag)
    return fvec


def jac(double [:] x, double [:] params):
    cdef cnp.ndarray[cnp.float64_t, ndim=1] x_arr = np.concatenate((x[::1], params[::1]))
    cdef int m = -1 # number of equations
    cdef int n = -1 # number of variables
    get_ne(&m)
    get_nx(&n)
    cdef cnp.ndarray[cnp.float64_t, ndim=1] fvec = \
        np.empty(m)
    cdef cnp.ndarray[cnp.float64_t, ndim=2, mode='fortran'] fjac = \
        np.empty((m,n), order='F')
    cdef int ldj = n # leading dimensino of Jacobian matrix
    cdef int iflag = 2 # Calculate Jacobian at x
    ldj = n
    func(&m, &n, &x_arr[0], &fvec[0], &fjac[0,0], &ldj, &iflag)
    return fjac
