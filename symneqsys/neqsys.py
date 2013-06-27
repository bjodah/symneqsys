
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


    @property
    def nx(self):
        return len(self.v)


    @property
    def nexprs(self):
        return len(self.exprs)


    @property
    def jac(self):
        return sympy.Matrix(
            self.nexprs, self.nx,
            lambda r, c: self.expr[r].diff(self.v[c]))


    def evaluate_residual(v_vals, param_vals):
        subsd = dict(zip(self.v, v_vals)+zip(self.params, param_vals))
        return np.array([expr.subs(subsd) for expr in self.exprs])


    def evaluate_jac(v_vals, param_vals):
        subsd = dict(zip(self.v, v_vals)+zip(self.params, param_vals))
        return np.array(
            [[cell.subs(subsd) for cell in row] for\
             row in self.jac.tolist()])


class SimpleNEQSys(object):
    """
    Lets a user create a NEQSys without manual instatiation of sympy.Symbol
    instances for variables and parameters. Instead, the user provide names
    as strings ("tokens")
    """

    pass
