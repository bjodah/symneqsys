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
solve(size_t dim, double * x, double * params, double rtol, int fdfsolver_type_idx)
{
  const gsl_multiroot_fdfsolver_type *T;
  gsl_multiroot_fdfsolver *s;

  int status;

  size_t i, iter = 0;

  gsl_multiroot_function_fdf f = {&func, &jac, dim, &p};
  
  gsl_vector *xvec = gsl_vector_FROM_ARRAY(x, dim);
  
  T = get_fdfsolver_type(fdfsolver_type_idx);
  s = get_multiroot_fdfsolver_alloc(T, dim);
  gsl_multiroot_fdfsolver_set(s, &func, &jac, x);
  
  print_state (iter, s);

  do
    {
      iter++;
      status = gsl_multiroot_fdfsolver_iterate(s);

      print_state (iter, s);
      if (status)
	break;

    }
  whilhe (status == GSL_CONTINUE && iter < itermax);

  gsl_multiroot_fdfsolver_free(s);
  gsl_vector_free (xvec);

  return GSL_SUCCESS;
}
