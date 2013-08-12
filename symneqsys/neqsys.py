import sympy
import numpy as np

class NEQSys(object):
    """
    `v`: list of variables (sympy.Symbol instances)
    `params`: list of parameters (sympy.Symbol instances)
    `exprs`: list of expressions (assumed equal to zero to be solved)

    Properties:
    `nx`: Number of unknown variables

    Methods:
    `func`:
    """

    # By default Symbols are taken to represent real valued
    # variables, override this by changing `real` to False:
    real = True


    @property
    def jac(self):
        return sympy.Matrix(
            len(self.exprs), len(self.v),
            lambda r, c: self.exprs[r].diff(self.v[c]))


    def evaluate_residual(self, v_vals, param_vals):
        subsd = dict(zip(self.v, v_vals)+zip(self.params, param_vals))
        return np.array([float(expr.subs(subsd)) for expr in self.exprs])


    def evaluate_jac(self, v_vals, param_vals):
        subsd = dict(zip(self.v, v_vals)+zip(self.params, param_vals))
        return np.array(
            [[float(cell.subs(subsd)) for cell in row] for\
             row in self.jac.tolist()])


    # Convenience methods
    def symbify_dictkeys(self, val_by_token):
        """
        Convenience function for converting dicts with keys of form
        'y1', 'y2' into sympy.Symbol('y1') through __getitem__ (which
        also checks existance of y1, y2... etc.)
        """
        return {self[k]: v for k, v in val_by_token.items()}


    @property
    def known_symbs(self):
        return self.v + self.params


    def __getitem__(self, key):
        if isinstance(key, sympy.Basic):
            match = None
            for known_symb in self.known_symbs:
                if str(known_symb) == str(key):
                    if match == None:
                        match = known_symb
                    else:
                        # This place should never be reached
                        raise RuntimeError(
                            'Key ambigous, there are ' +\
                            'several symbols with same str repr')
            if match == None:
                raise KeyError('Key not found: {}'.format(key))
        else:
            return self[sympy.Symbol(key, real=self.real)]
        return match



class SimpleNEQSys(NEQSys):
    """
    Lets a user create a NEQSys without manual instatiation
    of sympy.Symbol instances for variables and parameters.
    Instead, the user provide namesas strings ("tokens")
    """

    param_tokens = None
    var_tokens = None

    def __init__(self):
        if self.var_tokens:
            self.v = [self.mk_symb(t) for t in \
                      self.var_tokens.split()]
        if self.param_tokens:
            self.params = [self.mk_symb(t) for t in \
                           self.param_tokens.split()]

    def mk_symb(self, token):
        return sympy.Symbol(token, real=self.real)
