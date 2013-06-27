#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Solver(object):
    """
    Solver class taking a NEQSys instance as input
    """

    atol = None
    rtol = None

    def set_neqsys(self, neqsys):
        self._neqsys = neqsys

    def run(self, x0, maxiter=100):
        """
        Solves the neqsys
        store solution in self.solution with variable symbols as keys
        set success equal to True or False
        """
        pass

    def __getitem__(self, key):
        if self.num_result.success:
            try:
                return self.solution[key]
            except KeyError:
                return self.solution[self._neqsys[key]]


class SciPy_Solver(Solver):

    method = 'lm' # Least sqaure sense (linearly dep. rel. incl.)

    @property
    def options(self):
        return {'xtol' = self._atol}


    def run(self, x0, maxiter=100):
        import scipy.optimize

        self.num_result = scipy.optimize.root(
            fun = self._neqsys.evaluate_residual,
            x0 = x0,
            method = self.method,
            jac = self._neqsys.evaluate_jac,
            options = self.options)
