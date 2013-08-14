import time
import numpy as np
cimport numpy as cnp

from symneqsys.codeexport import Result

cdef extern int multiroot_solve(
    size_t dim, double * x, void * params, double atol,
    int fdfsolver_type_idx, int itermax, int print_,
    int store_intermediate, double * intermediate, int * iter,
    int * nfev_, int * njev_, int * nfjev_
)

cdef extern int c_func(
    size_t nx, double * x, double * params, double * out
)

cdef extern int c_jac(
    size_t nx, double * x, double * params, double * out
)

fdfsolver_types = ('newton', 'gnewton', 'hybridj', 'hybridsj')

def solve(double [:] x0, double [:] params, double atol,
          str solver_type = 'gnewton', int itermax=100):
    cdef double[:] x0_arr = x0.copy() # or np.ascontiguousarray ?
    cdef double[:] params_arr = params.copy() # or np.ascontiguousarray ?
    cdef cnp.ndarray[cnp.float64_t, ndim=1] intermediate = \
        np.empty(x0.shape[0]*itermax, order='C')
    cdef int status
    cdef int iter_, nfev, njev, nfjev
    start = time.time()
    status = _solve(x0_arr.shape[0], &x0_arr[0], &params_arr[0], atol,
                    fdfsolver_types.index(solver_type), itermax, 0, 1,
                    <double *> intermediate.data, &iter_, &nfev, &njev, &nfjev)
    end = time.time()
    return Result({
        'x': x0_arr,
        'success': status == 0,
        'status': status,
        'message': 'See gsl_errno.h',
        'fun': residuals(x0_arr, params_arr),
        'jac': jac(x0_arr, params_arr),
        'nfev': nfev,
        'njev': njev,
        'nit': iter_,
        'nfjev': nfjev, # <-- Special for GSL, combined func+jac callback
        'allvecs': intermediate.reshape((itermax, x0.shape[0]))[:iter_+1,:],
        'walltime': end-start,# only C-call, excluding compilation
    })


def residuals(double [:] x, double [:] params):
    cdef double[:] x_arr = x.copy()
    cdef double[:] params_arr = params.copy()
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out_arr = np.empty(x.shape[0], order='C')

    c_func(x.shape[0], &x_arr[0], &params_arr[0], &out_arr[0])
    return out_arr


def jac(double [:] x, double [:] params):
    cdef double[:] x_arr = x.copy()
    cdef double[:] params_arr = params.copy()
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out_arr = np.empty(x.shape[0]**2, order='C')

    c_jac(x.shape[0], &x_arr[0], &params_arr[0], &out_arr[0])

    return out_arr.reshape((x.shape[0], x.shape[0]))
