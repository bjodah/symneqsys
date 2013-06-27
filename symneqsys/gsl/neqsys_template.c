#include <gsl/gsl_matrix.h>
#include <gsl/gsl_errno.h>
#include <math.h>

// Python Mako template of C file
// Variables: f, cse_func
// Variables: jac, dfdt, NY, cse_jac
// CSE tokens: cse%d


int
func (const gsl_vector * x, void * params, gsl_vector * f)
{
  /*
    Best is to name all parameters k[0] ... k[P]
   */
  const double *k = (double *) params;

  /*
    Define variables for common subexpressions
   */
% for cse_token, cse_expr in cse_func:
  const double ${cse_token} = ${cse_expr};
% endfor

  /*
    Assign derivatives
   */
% for i, expr in enumerate(f):
  f[${i}] = ${expr};
% endfor

  return GSL_SUCCESS;
}


int
jac (const gsl_vector * x, void *params, gsl_matrix * J)
{
  const double *k = (double *) params;
  /*
    Define variables for common subexpressions
   */
% for cse_token, cse_expr in cse_jac:
  const double ${cse_token} = ${cse_expr};
% endfor


  /*
    Populate the NY times NY Jacobian matrix
   */
% for (i, j), expr in jac:
    gsl_matrix_set (J, ${i}, ${j}, ${expr});
% endfor

  return GSL_SUCCESS;
}


int
fdf (const gsl_vector * x, void *params, gsl_vector *f, gsl_matrix * J)
{
  func(x, params, f);
  jac(x, params, J);
  
  return GSL_SUCCESS;
}
