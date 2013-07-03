#include <stdio.h>

#include "solvers.h"
#include "neqsys.h"



gsl_multiroot_fdfsolver_type * get_fdfsolver_type(int index){
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
  const gsl_multiroot_fdfsolver_type *T = get_fdfsolver_type(fdfsolver_type_idx);
  gsl_multiroot_fdfsolver *s;


  gsl_multiroot_function_fdf f = {&func, &jac, &fdf, dim, params};
  
  gsl_block xblk = {dim, x}; // we already have a contigous x-array passed into function
  gsl_vector xvec = {dim, 1, x, &xblk, 0};
  
  s = gsl_multiroot_fdfsolver_alloc(T, dim);
  gsl_multiroot_fdfsolver_set(s, &f, &xvec);

  int iter = 0;
  int status;
  gsl_set_error_handler_off(); // Don't abort the program upon errors

  print_state(iter, s, dim);

  do
    {
      iter++;
      status = gsl_multiroot_fdfsolver_iterate(s);

      print_state(iter, s, dim);
      if (status)
	break;

      status = gsl_multiroot_test_residual(s->f, atol);
    }
  while (status == GSL_CONTINUE && iter < itermax);

  gsl_multiroot_fdfsolver_free(s);

  return status;
}


void
print_state (int iter, gsl_multiroot_fdfsolver * s, size_t dim)
{
  int i;
  printf ("iter = %3u", iter);
  for (i=0; i < (int)dim; ++i){
    printf("% .3f % .3f",   
	   gsl_vector_get (s->x, i),
	   gsl_vector_get (s->f, i)
	   );
  }
}

void c_func(size_t nx, double * x, double * params, double * out){
  gsl_block xblk = {nx, x}; // we already have a contigous x-array passed into function
  gsl_vector xvec = {nx, 1, x, &xblk, 0};

  gsl_block outblk = {nx, out}; // we already have a contigous x-array passed into function
  gsl_vector outvec = {nx, 1, out, &outblk, 0};

  func(&xvec, params, &outvec);
}

void c_jac(size_t nx, double * x, double * params, double * out){
  gsl_block xblk = {nx, x}; // we already have a contigous x-array passed into function
  gsl_vector xvec = {nx, 1, x, &xblk, 0};

  gsl_block outblk = {nx*nx, out}; // we already have a contigous x-array passed into function
  gsl_matrix outmat = {nx, nx, nx, out, &outblk, 0};

  jac(&xvec, params, &outmat);
}
