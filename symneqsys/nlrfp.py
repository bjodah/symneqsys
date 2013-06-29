from collections import OrderedDict

class NLRFP(object):
    """
    Non-linear Root Finding Problem class
    Can perform variable substitution and scaling for
    achieving better condition of e.g. Jacboian matrix
    during the numerical treatment of the problem.

    More user friendly than Solver class (dicts instead
    of lists as input e.g.)
    """

    def __init__(self, neqsys, params=None,
                 guess=None, solver=None, inv_trnsfm=None,
                 scaling=None):
        """
        guess 1.0 for all v if None
        """
        self._neqsys = neqsys

        # store params (default 1.0)
        if params == None:
            self.params = {k: 1.0 for k in self._neqsys.v}
        else:
            self.params = self._neqsys.symbify_dictkeys(params)
            assert all([self._neqsys[k] in self._neqsys.params for \
                        k in self.params])

        # store guess (default 1.0)
        if guess == None:
            self.guess = {k: 1.0 for k in self._neqsys.v}
        else:
            self.guess = self._neqsys.symbify_dictkeys(guess)
            assert all([self._neqsys[k] in self._neqsys.v for \
                        k in self.guess])

        # Assign solver, and set to current neqsys
        self.solver = solver or SciPy_Solver()
        self.solver.set_neqsys(self._neqsys)

        self._inv_trnsfm = inv_trnsfm
        self._scaling = scaling


    @property
    def solution(self):
        """
        Abstracts away variable substitutions and scaling used
        in the numerical treatment of the problem

        Returns an OrderedDict of the final values.
        """
        if self._inv_trnsfm:
            raise NotImplementedError
        else:
            return self._rescale(OrderedDict(zip(
                self._neqsys.v, self.solver.num_result.x)))


    def _rescale(self, values):
        if self._scaling:
            return OrderedDict((k, v*self._scaling[k]) for k, v in \
                                values.items())
        else:
            return values


    def use_internal_trnsfm(self, trnsfm, inv_trnsfm):
        if self._scaling: raise RuntimeError('Scale after transform.')
        pass


    def use_internal_scaling(self, scaling):
        pass


    def solve(self, maxiter=100):
        """
        Attempts to numerically solve the problem using
        the Solver subclass instance.

        Returns success (True/False)
        """
        x0_vals = [self.guess[k] for k in self._neqsys.v]
        param_vals = [self.params[k] for k in self._neqsys.params]
        self.solver.run(x0_vals, param_vals, maxiter)
        return self.solver.num_result.success


    def plot_convergence(self):
        """
        """
        pass
