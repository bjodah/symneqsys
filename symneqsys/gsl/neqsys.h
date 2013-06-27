#ifndef _NEQSYS_H_
#define _NEQSYS_H_

int
func (const gsl_vector * x, void * params, gsl_vector * f);

int
jac (const gsl_vector * x, void *params, gsl_matrix * J);

int
fdf (const gsl_vector * x, void *params, gsl_vector *f, gsl_matrix * J);

#endif
