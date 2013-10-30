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
        else:
            self.v = []

        if self.param_tokens:
            self.params = [self.mk_symb(t) for t in \
                           self.param_tokens.split()]
        else:
            self.params = []

    def is_unused(self, name):
        try:
            symb = self[name]
        except KeyError:
            return True
        return False

    def add_idx(self, token):
        if self._indices == None: self._indices = []
        idx = sympy.Idx(token)
        if not idx in self._indices:
            self._indices.append(idx)
        else:
            assert self[token] == idx
        return idx

    def mk_symb(self, token):
        if '[' in token:
            # IndexedBase
            assert ']' in token
            name, the_rest = token.split('[')
            idx_strs = map(str.strip, the_rest.split(']')[0].split())
            idxs = map(self.add_idx, idx_strs)
            assert self.is_unused(name)
            return sympy.Indexed(name, *idxs)
        else:
            return sympy.Symbol(token, real=self.real)

#']')            ]            ]
