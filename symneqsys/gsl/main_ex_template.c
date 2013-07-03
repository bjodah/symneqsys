#include <stdlib.h>
#include "solvers.h"

int
main(int argc, char **argv)
{
  size_t dim = ${NX};
  double x[] = {${', '.join([str(1.0/(i+1.0)) for i in range(NX)])}};
  double params[] = {${', '.join(['1.0']*NPARAMS)}};
  double atol = 1e-8;
  int fdfsolver_type_idx = 0;
  int itermax = 100;
  _solve(dim, x, params, atol, fdfsolver_type_idx, itermax);
}
