from collections import OrderedDict

import numpy as np
from .solver import SciPy_Solver


class Problem(object):
    """
    Non-linear Root Finding Problem class
    Can perform variable substitution (could be simple scaling) for
    achieving better condition of e.g. Jacboian matrix
    during the numerical treatment of the problem.

    More user friendly than Solver class (dicts instead
    of lists as input e.g.)
    """

    def __init__(self, neqsys, params=None,
                 guess=None, solver=None, inv_trnsfm=None):
        """
        guess 1.0 for all v if None
        """
        self._neqsys = neqsys

        assert len(neqsys.exprs) >= len(neqsys.v)

        # store params (default 1.0)
        if params is None:
            self.params = {k: 1.0 for k in self._neqsys.params}
        else:
            self.params = self._neqsys.symbify_dictkeys(params)
            assert all([self._neqsys[k] in self._neqsys.params for
                        k in self.params])

        # store guess (default 1.0)
        if guess is None:
            self.guess = {k: 1.0 for k in self._neqsys.v}
        else:
            self.guess = self._neqsys.symbify_dictkeys(guess)
            assert all([self._neqsys[k] in self._neqsys.v for
                        k in self.guess])

        # Assign solver, and set to current neqsys
        self.solver = solver or SciPy_Solver()
        self.solver.set_neqsys(self._neqsys)

        self._inv_trnsfm = inv_trnsfm

        # Check for singlarity if number of expressions
        # does not exceed the number of variables
        if len(self._neqsys.exprs) == len(self._neqsys.v):
            assert not self.check_jac_singular()

    def check_jac_singular(self):
        from scipy import linalg
        try:
            linalg.inv(self._neqsys.evaluate_jac(
                self.x0_array, self.params_array))
        except linalg.LinAlgError:
            return True
        return False

    @property
    def solution(self):
        """
        Abstracts away variable substitutions used
        in the numerical treatment of the problem

        Returns an OrderedDict of the final values.
        """
        if self._inv_trnsfm:
            raise NotImplementedError
        return OrderedDict(zip(
            self._neqsys.v, self.solver.num_result.x))

    def use_internal_trnsfm(self, trnsfm, inv_trnsfm):
        pass

    @property
    def x0_array(self):
        return np.array([self.guess[k] for k in self._neqsys.v],
                        dtype=np.float64)

    @property
    def params_array(self):
        return np.array([self.params[k] for k in self._neqsys.params],
                        dtype=np.float64)

    def solve(self, itermax=100, **kwargs):
        """
        Attempts to numerically solve the problem using
        the Solver subclass instance.

        additional keyword arguments are passed on to solver

        Returns success (True/False)
        """
        for attr in ('abstol', 'reltol'):
            if attr in kwargs:
                setattr(self, attr, kwargs.pop('abstol'))
        self.solver.run(self.x0_array, self.params_array, itermax, **kwargs)
        return self.solver.num_result.success

    def plot_convergence(self):
        """
        """
        pass
