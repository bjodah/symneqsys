import time
import numpy as np
cimport numpy as cnp

from symneqsys.codeexport import Result

cdef extern void lm_solve(double * x, double * tol, int * info)

cdef extern void func(
    int * m, int * n, double * x, double * f, int * ldj, int * iflag
)


def solve(double [:] x0, double [:] params, double atol,
          str solver_type = 'lm', int itermax=100):
    cdef double[:] x0_arr = x0.copy() # or np.ascontiguousarray ?
    cdef double[:] params_arr = params.copy() # or np.ascontiguousarray ?
    cdef cnp.ndarray[cnp.float64_t, ndim=1] x_and_param = \
        np.empty(x0.shape[0]+params.shape[0])
    cdef int nfev, njev, status
    start = time.time()
    lm_solve(&x_and_param[0], &atol, &status)
    #status = _solve(x0_arr.shape[0], &x0_arr[0], &params_arr[0], atol,
             #       fdfsolver_types.index(solver_type), itermax, 0, 1,
             #       <double *> intermediate.data, &iter_, &nfev, &njev, &nfjev)

    end = time.time()
    get_nfev(&nfev)
    get_njev(&njev)
    return Result({
        'x': x0_arr,
        'success': status == 0,
        'status': info,
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
    cdef double[:] x_arr = x.copy()
    cdef double[:] params_arr = params.copy()
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out_arr = np.empty(x.shape[0], order='C')

    func(x.shape[0], &x_arr[0], &params_arr[0], &out_arr[0])
    return out_arr


def jac(double [:] x, double [:] params):
    cdef double[:] x_arr = x.copy()
    cdef double[:] params_arr = params.copy()
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out_arr = np.empty(x.shape[0]**2, order='C')

    func(x.shape[0], &x_arr[0], &params_arr[0], &out_arr[0])

    return out_arr.reshape((x.shape[0], x.shape[0]))
