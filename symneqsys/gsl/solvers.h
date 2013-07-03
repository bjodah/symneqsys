#ifndef _SOLVERS_H_
#define _SOLVERS_H_

#include <gsl/gsl_errno.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_multiroots.h>


gsl_multiroot_fdfsolver_type * get_fdfsolver_type(int index);

int
_solve(size_t dim, double * x, void * params, double atol, int fdfsolver_type_idx, int itermax);

void
print_state (int iter, gsl_multiroot_fdfsolver * s, size_t dim);

void c_func(size_t nx, double * x, double * params, double * out);

void c_jac(size_t nx, double * x, double * params, double * out);

#endif
