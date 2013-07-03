#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial


class Solver(object):
    """
    Solver class taking a NEQSys instance as input
    """

    abstol = 1e-6
    reltol = 1e-6

    solve_args = {} # speical keyword arguments to run in subclasses

    def set_neqsys(self, neqsys):
        self._neqsys = neqsys


    def run(self, x0, params, itermax=100, **kwargs):
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
        return {'xtol': self.abstol}


    def run(self, x0, params, itermax=100):
        import scipy.optimize

        self.num_result = scipy.optimize.root(
            fun = partial(self._neqsys.evaluate_residual,
                          param_vals=params),
            x0 = x0,
            method = self.method,
            jac = partial(self._neqsys.evaluate_jac,
                          param_vals=params),
            options = self.options)
