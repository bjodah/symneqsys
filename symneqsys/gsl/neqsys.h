#ifndef _NEQSYS_H_
#define _NEQSYS_H_

extern int NFEV, NJEV, NFJEV; // Count number of calls 


int
func (const gsl_vector * x, void * params, gsl_vector * f);

int
jac (const gsl_vector * x, void *params, gsl_matrix * J);

int
fdf (const gsl_vector * x, void *params, gsl_vector *f, gsl_matrix * J);

#endif
