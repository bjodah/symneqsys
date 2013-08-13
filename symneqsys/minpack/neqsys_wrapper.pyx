# MINPACK wrapper for symneqsys

import time
import numpy as np
cimport numpy as cnp

from symneqsys.codeexport import Result

cdef extern void lm_solve(double * x, double * tol, int * info)

cdef extern void func(
    int * m, int * n, double * x, double * f, double * j, int * ldfjac, int * iflag
)

cdef extern void get_nfev(int * nfev)
cdef extern void get_njev(int * njev)
cdef extern void get_ne(int * ne_)
cdef extern void get_nx(int * nx_)

# lmder1_info is from lmder1.f
lmder1_info = {
    0: 'improper input parameters.',
    1: 'algorithm estimates that the relative error in the sum of squares is at most tol.',
    2: 'algorithm estimates that the relative error between x and the solution is at most tol.',
    3: 'conditions for info = 1 and info = 2 both hold.',
    4: 'fvec is orthogonal to the columns of the jacobian to machine precision.',
    5: 'number of calls to fcn with iflag = 1 has reached 100*(n+1).',
    6: 'tol is too small. no further reduction in the sum of squares is possible.',
    7: 'tol is too small. no further improvement in the approximate solution x is possible.',
}

def solve(double [:] x0, double [:] params, double tol,
          str solver_type = 'lm', int itermax=100):
    """
    Solve using Levenberg-Marquardt algorithm
    """
    cdef cnp.ndarray[cnp.float64_t, ndim=1] x_arr = np.concatenate((x0[::1], params[::1]))
    cdef int nfev, njev, status

    start = time.time()
    lm_solve(&x_arr[0], &tol, &status)
    end = time.time()
    get_nfev(&nfev)
    get_njev(&njev)

    return Result({
        'x': x_arr[:x0.size],
        'success': status == 1 or status == 2 or status == 3,
        'status': status,
        'message': lmder1_info[status],
        'fun': residuals(x0, params),
        'jac': jac(x0, params),
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
    cdef int ldfjac = n # leading dimensino of Jacobian matrix
    cdef int iflag = 1 # Calculate functions at x
    get_ne(&m)
    get_nx(&n)
    ldfjac = n
    func(&m, &n, &x_arr[0], &fvec[0], &fjac[0,0], &ldfjac, &iflag)
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
    cdef int ldfjac = n # leading dimension of Jacobian matrix
    cdef int iflag = 2 # Calculate Jacobian at x
    ldfjac = n
    func(&m, &n, &x_arr[0], &fvec[0], &fjac[0,0], &ldfjac, &iflag)
    return fjac
