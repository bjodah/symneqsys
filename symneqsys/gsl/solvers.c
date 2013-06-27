#include <stdio.h>

#include <gsl/gsl_errno.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_multiroots.h>

#include "drivers.h"
#include "neqsys.h"



const gsl_multiroot_fdfsolver_type * get_fdfsolver_type(int index){
  switch(index){
  case 0:
    return gsl_multiroot_fdfsolver_newton;
  case 1:
    return gsl_multiroot_fdfsolver_gnewton;
  case 2:
    return gsl_multiroot_fdfsolver_hybridj;
  case 3:
    return gsl_multiroot_fdfsolver_hybridsj;
  default:
    return gsl_multiroot_fdfsolver_newton;
  }
}


int
_solve(size_t dim, double * x, void * params, double atol, int fdfsolver_type_idx, int itermax)
{
  // TODO: store intermediate steps and store in an output arg.
  const gsl_multiroot_fdfsolver_type *T;
  gsl_multiroot_fdfsolver *s;

  int status;

  size_t iter = 0;

  gsl_multiroot_function_fdf f = {&func, &jac, &fdf, dim, params};
  
  gsl_block xblk = {dim, x}; // we already have a contigous x-array passed into function
  gsl_vector xvec = {dim, 1, x, xblk, 0};
  
  T = get_fdfsolver_type(fdfsolver_type_idx);
  s = get_multiroot_fdfsolver_alloc(T, dim);
  gsl_multiroot_fdfsolver_set(s, &f, &xvec);
  
  print_state(iter, s);

  do
    {
      iter++;
      status = gsl_multiroot_fdfsolver_iterate(s);

      print_state(iter, s);
      if (status)
	break;

      status = gsl_multiroot_test_residual(s->f, atol)
    }
  while (status == GSL_CONTINUE && iter < itermax);

  gsl_multiroot_fdfsolver_free(s);

  return GSL_SUCCESS;
}
