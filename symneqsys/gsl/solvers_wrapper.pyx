import numpy as np
cimport numpy as cnp

cdef extern int _solve(
    size_t dim, double * x, void * params, double atol,
    int fdfsolver_type_idx, int itermax);

fdfsolver_types = ('newton', 'gnewton', 'hybridj', 'hybridsj')

def solve(double [:] x0, double [:] params, double atol,
          str solver_type = 'gnewton', int intermax=100):
    cdef np.ndarray[np.float64_t, ndim=1] x_arr = np.ascontiguousarray(x0)
    cdef np.ndarray[np.float64_t, ndim=1] params_arr = np.ascontiguousarray(params)

    _solve(x_arr.shape[0], &x_arr[0], &params_arr[0], atol,
           fdfsolver_types.index(solver_type), itermax)

    return x_arr
