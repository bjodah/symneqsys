import numpy as np
cimport numpy as cnp

from cython_gsl cimport gsl_vector

cdef extern int _solve(
    size_t dim, double * x, void * params, double atol,
    int fdfsolver_type_idx, int itermax)

cdef extern int c_func(
    size_t nx, double * x, double * params, double * out
)

cdef extern int c_jac(
    size_t nx, double * x, double * params, double * out
)

fdfsolver_types = ('newton', 'gnewton', 'hybridj', 'hybridsj')

def solve(double [:] x0, double [:] params, double atol,
          str solver_type = 'gnewton', int itermax=100):
    cdef double[:] x0_arr = x0.copy() # ensure contiguous
    cdef double[:] params_arr = params.copy() # ensure contiguous
    cdef int status

    status = _solve(x0_arr.shape[0], &x0_arr[0], &params_arr[0], atol,
                    fdfsolver_types.index(solver_type), itermax)

    return status, x0_arr
    # cdef cnp.ndarray[cnp.float64_t, ndim=1] x_arr = np.ascontiguousarray(x0)
    # cdef cnp.ndarray[cnp.float64_t, ndim=1] params_arr = np.ascontiguousarray(params)


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
