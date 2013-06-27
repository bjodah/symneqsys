#ifndef _SOLVERS_H_
#define _SOLVERS_H_

const gsl_multiroot_fdfsolver_type * get_fdfsolver_type(int index);

int
_solve(size_t dim, double * x, void * params, double atol, int fdfsolver_type_idx, int itermax);

#endif
