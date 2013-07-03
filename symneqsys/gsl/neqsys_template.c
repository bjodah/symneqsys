#include <gsl/gsl_matrix.h>
#include <gsl/gsl_errno.h>
#include <math.h>

#include "neqsys.h"
// Python Mako template of C file

// Global counters
int NFEV = 0;
int NJEV = 0;
int NFJEV = 0;

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
    Calculate residuals
   */
% for i, expr in enumerate(func_new_code):
  gsl_vector_set(f, ${i}, ${expr});
% endfor

  NFEV++;
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

  NJEV++;
  return GSL_SUCCESS;
}


int
fdf (const gsl_vector * x, void *params, gsl_vector *f, gsl_matrix * J)
{
  const double *k = (double *) params;
  const double * const y = (double *) x->data;

  /*
    Define variables for common subexpressions
   */
% for cse_token, cse_expr in fj_cse_defs:
  const double ${cse_token} = ${cse_expr};
% endfor

  /*
    Calculate residuals
   */
% for i, expr in enumerate(fj_func_new_code):
  gsl_vector_set(f, ${i}, ${expr});
% endfor


  /*
    Populate the NY times NY Jacobian matrix
   */
% for i, expr in enumerate(fj_jac_new_code):
  gsl_matrix_set (J, ${i // NX}, ${i % NX}, ${expr});
% endfor

  
  NFJEV++;
  return GSL_SUCCESS;
}
