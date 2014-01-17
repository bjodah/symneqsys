import time
import numpy as np
cimport numpy as cnp

from symneqsys.codeexport import Result

cdef extern int solve_multiroot(
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

multiroot_solver_types = ('newton', 'gnewton', 'hybridj', 'hybridsj')

def solve(double [::1] x0, double [::1] params, double atol,
          str solver_type = 'gnewton', int itermax=100):
    cdef cnp.ndarray[cnp.float64_t, ndim=1] intermediate = \
        np.empty(x0.shape[0]*itermax, order='C')
    cdef int status
    cdef int iter_, nfev, njev, nfjev
    cdef double * params_pointer = &params[0] if len(params) > 0 else NULL
    start = time.time()
    status = solve_multiroot(x0.shape[0], &x0[0], params_pointer, atol,
                             multiroot_solver_types.index(solver_type), itermax, 0, 1,
                             <double *>intermediate.data, &iter_, &nfev, &njev, &nfjev)
    end = time.time()
    return Result({
        'x': np.array(x0),
        'success': status == 0,
        'status': status,
        'message': 'See gsl_errno.h',
        'fun': residuals(x0, params),
        'jac': jac(x0, params),
        'nfev': nfev,
        'njev': njev,
        'nit': iter_,
        'nfjev': nfjev, # <-- Special for GSL, combined func+jac callback
        'allvecs': intermediate.reshape((itermax, x0.shape[0]))[:iter_+1,:],
        'walltime': end-start,# only C-call, excluding compilation
    })


def residuals(double [::1] x, double [::1] params):
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out_arr = np.empty(x.shape[0], order='C')
    cdef double * params_pointer = &params[0] if len(params) > 0 else NULL

    c_func(x.shape[0], &x[0], params_pointer, &out_arr[0])
    return out_arr


def jac(double [::1] x, double [::1] params):
    cdef cnp.ndarray[cnp.float64_t, ndim=1] out_arr = np.empty(x.shape[0]**2, order='C')
    cdef double * params_pointer = &params[0] if len(params) > 0 else NULL
    c_jac(x.shape[0], &x[0], params_pointer, &out_arr[0])
    return out_arr.reshape((x.shape[0], x.shape[0]))
