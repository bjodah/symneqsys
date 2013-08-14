#include <stdlib.h>
#include "solvers.h"


%if NE == NX:
int
main(int argc, char **argv)
{
  size_t dim = ${NX};
  double x[] = {${', '.join([str(1.0/(i+1.0)) for i in range(NX)])}};
  double params[] = {${', '.join(['1.0']*NPARAMS)}};
  double atol = 1e-8;
  int multiroot_fdfsolver_type_idx = 0;
  int itermax = 100;
  int nfev, njev, nfjev;
  solve_multiroot(dim, x, params, atol, multi_fdfsolver_type_idx, itermax,
		  1, 0, NULL, &iter, &nfev, &njev, &nfjev);
}
%else:
int
main(int argc, char **argv)
{
  size_t ne = ${NE};
  size_t nx = ${NX};
  double x[] = {${', '.join([str(1.0/(i+1.0)) for i in range(NX)])}};
  double params[] = {${', '.join(['1.0']*NPARAMS)}};
  double atol = 1e-8;
  double rtol = 1e-8;
  int multifit_fdfsolver_type_idx = 0;
  int itermax = 100;
  int nfev, njev, nfjev;
  solve_multifit(ne, nx, x, params, atol, rtol, multifit_fdfsolver_type_idx,
		 itermax, 3, 1, 0, NULL, &iter, &nfev, &nfjev);
}
%endif
