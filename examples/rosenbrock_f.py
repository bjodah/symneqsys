
class Rosenbrock(SimpleNEQSys):
    param_tokens = 'a b'
    var_tokens = 'x0 x1'

    @property
    def exprs(self):
        x0, x1, a, b = [getattr(self, attr) for attr \
                        in ('x0', 'x1', 'a', 'b')]
