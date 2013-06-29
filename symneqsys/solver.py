#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial


class Solver(object):
    """
    Solver class taking a NEQSys instance as input
    """

    _atol = 1e-6
    _rtol = 1e-6


    def set_neqsys(self, neqsys):
        self._neqsys = neqsys


    def run(self, x0, params, maxiter=100):
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
        return {'xtol': self._atol}


    def run(self, x0, params, maxiter=100):
        import scipy.optimize

        self.num_result = scipy.optimize.root(
            fun = partial(self._neqsys.evaluate_residual,
                          param_vals=params),
            x0 = x0,
            method = self.method,
            jac = partial(self._neqsys.evaluate_jac,
                          param_vals=params),
            options = self.options)
