
class Solver(object):
    """
    Solver class taking a NEQSys instance as input
    """

    atol = None
    rtol = None
    solution = None
    success = None

    def __init__(self, neqsys):
        self._neqsys = neqsys


    def solve(self, maxiter=100):
        """
        Solves the neqsys
        store solution in self.solution with variable symbols as keys
        set success equal to True or False
        """
        pass


    def __getitem__(self, key):
        if self.success == None:
            raise RuntimeError('Success flag have not been set, have solve method been run?')
        if self.success == False:
            raise RuntimeError('The previous solve invocation failed. (the success attribute == False)')
        if self.solution == None:
            raise RuntimeError('No solution in Solver, please report a bug.')

        try:
            return self.solution[key]
        except KeyError:
            return self.solution[self._neqsys[key]]
