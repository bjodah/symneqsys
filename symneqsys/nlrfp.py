

class NLRFP(object):
    """
    Non-linear Root Finding Problem class
    Can perform variable substitution and scaling for
    achieving better condition of e.g. Jacboian matrix
    during the numerical treatment of the problem.
    """

    def __init__(self, neqsys, param_vals, guess=None, solver=None):
        self._neqsys = neqsys
        self.param_vals = param_vals
        self.guess = guess or np.ones(neqsys.nx)
        self.solver = solver
        self.solver.set_neqsys(self._neqsys)


    @property
    def solution(self):
        """
        Abstracts away variable substitutions and scaling used
        in the numerical treatment of the problem
        """
        pass


    def use_internal_trnsfm(self, trnsfm, inv_trsfm):
        pass


    def use_internal_scaling(self, scaling):
        pass


    def solve(self, x0, maxiter=100):
        self.solver.run(x0, maxiter)
        return self.solver.num_result.success

    def plot_convergence(self):
        """
        """
        pass
