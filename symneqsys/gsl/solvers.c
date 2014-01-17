#include <stdio.h>

#include "solvers.h"
#include "neqsys.h"


const gsl_multiroot_fdfsolver_type * get_multiroot_fdfsolver_type(int index){
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
solve_multiroot(size_t dim, double * x, void * params, double atol,
		int multiroot_fdfsolver_type_idx, int itermax, int print_, 
		int store_intermediate, double * intermediate, 
		int * iter, int * nfev_, int * njev_, int * nfjev_)
{
  int status;

  const gsl_multiroot_fdfsolver_type *T = get_multiroot_fdfsolver_type(multiroot_fdfsolver_type_idx);
  gsl_multiroot_fdfsolver *s = gsl_multiroot_fdfsolver_alloc(T, dim);
  gsl_multiroot_function_fdf f = {&func, &jac, &fdf, dim, params};
  gsl_block xblk = {dim, x}; // we already have a contigous x-array passed into function
  gsl_vector xvec = {dim, 1, x, &xblk, 0};
  gsl_multiroot_fdfsolver_set(s, &f, &xvec);

  *iter = 0;
  // (re)set globals in neqsys.h
  NFEV = 0;
  NJEV = 0;
  NFJEV = 0;

  gsl_set_error_handler_off(); // Don't abort the program upon errors

  if (store_intermediate){
    for (size_t i=0; i<dim; ++i){
      intermediate[(*iter)*dim+i] = gsl_vector_get(s->x, i);
    }
  }
  if (print_)
    print_multiroot_state(*iter, s, dim);

  do
    {
      (*iter)++;
      status = gsl_multiroot_fdfsolver_iterate(s);
      
      if (store_intermediate){
	for (size_t i=0; i<dim; ++i){
	  intermediate[(*iter)*dim+i] = gsl_vector_get(s->x, i);
	}
      }
      if (print_)
	print_multiroot_state(*iter, s, dim);
      if (status)
	break;

      status = gsl_multiroot_test_residual(s->f, atol);
    }
  while (status == GSL_CONTINUE && *iter < itermax-1);

  // Store global counters, see neqsys.h
  *nfev_ = NFEV;
  *njev_ = NJEV;
  *nfjev_ = NFJEV;

  if (status == GSL_SUCCESS)
    gsl_vector_memcpy(&xvec, s->x);

  gsl_multiroot_fdfsolver_free(s);

  return status;
}

const gsl_multifit_fdfsolver_type * get_multifit_fdfsolver_type(int index){
  switch(index){
  case 0:
    return gsl_multifit_fdfsolver_lmsder; // Scaled modified Levenberg-Marquardt
  case 1:
    return gsl_multifit_fdfsolver_lmder; // (Unscaled) modified Levenberg-Marquardt
  default:
    return gsl_multifit_fdfsolver_lmsder; // Scaled modified Levenberg-Marquardt
  }
}

int
solve_multifit(size_t ne, size_t nx, double * x, void * params, 
	       double atol, double rtol, int multifit_fdfsolver_type_idx,
	       int itermax, int criterion, int print_, int store_intermediate, 
	       double * intermediate, int * iter, int * nfev_, int * njev_, int * nfjev_)
{
  // criterion:
  //     1:  gsl_multifit_test_delta
  //     2:  gsl_multifit_test_gradient
  //     3:  Both 1 & 2

  int status;

  const gsl_multifit_fdfsolver_type *T = get_multifit_fdfsolver_type(multifit_fdfsolver_type_idx);
  gsl_multifit_fdfsolver *s = gsl_multifit_fdfsolver_alloc(T, ne, nx);
  gsl_multifit_function_fdf f = {&func, &jac, &fdf, ne, nx, params};
  gsl_block xblk = {nx, x}; // we already have a contigous x-array passed into function
  gsl_vector xvec = {nx, 1, x, &xblk, 0};
  gsl_multifit_fdfsolver_set(s, &f, &xvec);
  gsl_vector * g = NULL;

  *iter = 0;
  // (re)set globals in neqsys.h
  NFEV = 0;
  NJEV = 0;
  NFJEV = 0;

  gsl_set_error_handler_off(); // Don't abort the program upon errors
    // (we are responsible for acting on status codes returned by the routines)

  if (store_intermediate){
    for (size_t i=0; i<nx; ++i){
      intermediate[(*iter)*nx+i] = gsl_vector_get(s->x, i);
    }
  }
  if (print_)
    print_multifit_state(*iter, s, nx, ne);

  do
    {
      (*iter)++;
      status = gsl_multifit_fdfsolver_iterate(s);
      
      if (store_intermediate){
	for (size_t i=0; i<nx; ++i){
	  intermediate[(*iter)*nx+i] = gsl_vector_get(s->x, i);
	}
      }
      if (print_)
	print_multifit_state(*iter, s, nx, ne);
      if (status)
	break;

      // Handle criterion option
      switch(criterion){
      case 1:
	status = gsl_multifit_test_delta(s->dx, s->x, atol, rtol);
      default:
	g = gsl_vector_alloc(ne);
	gsl_multifit_gradient(s->J, s->f, g);
	int gradient_status = gsl_multifit_test_gradient(g, atol);
	switch(criterion){
	case 2:
	  status = gradient_status;
	case 3:
	  if (status == GSL_SUCCESS){
	    int delta_status = gsl_multifit_test_delta(s->dx, s->x, atol, rtol);
	    if (delta_status != GSL_SUCCESS)
	      status = delta_status;
	  }
	}
      }
    }
  while (status == GSL_CONTINUE && *iter < itermax-1);

  // Store global counters, see neqsys.h
  *nfev_ = NFEV;
  *njev_ = NJEV;
  *nfjev_ = NFJEV;

  if (status == GSL_SUCCESS)
    gsl_vector_memcpy(&xvec, s->x);

  gsl_multifit_fdfsolver_free(s);

  return status;
}


void
print_multiroot_state (int iter, gsl_multiroot_fdfsolver * s, size_t dim)
{
  int i;
  printf ("iter = %3u\n", iter);
  for (i=0; i < (int)dim; ++i){
    printf("% .5f % .5f",   
	   gsl_vector_get (s->x, i),
	   gsl_vector_get (s->f, i)
	   );
  }
  printf("\n");
}

void
print_multifit_state (int iter, gsl_multifit_fdfsolver * s, size_t nx, size_t ne)
{
  printf("%3u ", iter);
  for (size_t i=0; i < nx; ++i){
    printf("% .5f ", gsl_vector_get (s->x, i));
  }
  for (size_t i=0; i < ne; ++i){
    printf("% .5f ", gsl_vector_get (s->f, i));
  }
  printf("\n");
}


// The functions below are convenience functions when we have aldreay allocated
// space for the data.

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
