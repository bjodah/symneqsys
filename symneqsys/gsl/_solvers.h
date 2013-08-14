#ifndef __SOLVERS_H_
#define __SOLVERS_H_


#include <gsl/gsl_errno.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_multiroots.h>


const gsl_multiroot_fdfsolver_type * get_multiroot_fdfsolver_type(int index);

int
solve_multiroot(size_t dim, double * x, void * params, double atol,
		int multiroot_fdfsolver_type_idx, int itermax, int print_,
		int store_intermediate, double * intermediate, int * iter,
		int * nfev_, int * njev_, int * nfjev_);

void
print_multiroot_state (int iter, gsl_multiroot_fdfsolver * s, size_t dim);

int
solve_multifit(size_t ne, size_t nx, double * x, void * params, 
	       double atol, double rtol, int multifit_fdfsolver_type_idx,
	       int itermax, int criterion, int print_, int store_intermediate, 
	       double * intermediate, int * iter, int * nfev_, int * nfjev_);

void
print_multifit_state (int iter, gsl_multifit_fdfsolver * s, size_t nx, size_t ne);


void
c_func(size_t nx, double * x, double * params, double * out);

void
c_jac(size_t nx, double * x, double * params, double * out);

#endif
