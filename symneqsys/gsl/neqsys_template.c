#include <gsl/gsl_matrix.h>
#include <gsl/gsl_errno.h>
#include <math.h>

// Python Mako template of C file


int
func (const gsl_vector * x, void * params, gsl_vector * f)
{
  /*
    Best is to name all parameters k[0] ... k[P]
   */
  const double *k = (double *) params;
  const double * const y = (double *) x->data;

  /*
    Define variables for common subexpressions
   */
% for cse_token, cse_expr in func_cse_defs:
  const double ${cse_token} = ${cse_expr};
% endfor

  /*
    Assign derivatives
   */
% for i, expr in enumerate(func_new_code):
  gsl_vector_set(f, ${i}, ${expr});
% endfor

  return GSL_SUCCESS;
}


int
jac (const gsl_vector * x, void *params, gsl_matrix * J)
{
  const double *k = (double *) params;
  const double * const y = (double *) x->data;

  /*
    Define variables for common subexpressions
   */
% for cse_token, cse_expr in jac_cse_defs:
  const double ${cse_token} = ${cse_expr};
% endfor


  /*
    Populate the NY times NY Jacobian matrix
   */
% for i, expr in enumerate(jac_new_code):
  gsl_matrix_set (J, ${i // NX}, ${i % NX}, ${expr});
% endfor

  return GSL_SUCCESS;
}


int
fdf (const gsl_vector * x, void *params, gsl_vector *f, gsl_matrix * J)
{
  int i, j;
  func(x, params, f);
  jac(x, params, J);
  printf("%d\n",f->size);
  for (i=0; i < f->size; ++i){
    for (j=0; j < f->size; ++j){
      printf("%.3f ", gsl_matrix_get(J, i, j));
    }
    printf("%.3f\n", gsl_vector_get(f,i));
  }
  
  return GSL_SUCCESS;
}
