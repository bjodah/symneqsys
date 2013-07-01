from itertools import chain

from pycompilation.codeexport import Generic_Code
from symneqsys.solver import Solver

class NEQSys_Code(Generic_Code):
    """
    Wraps some sympy functionality of code generation from matrices
    returned by NEQSys.evaluate_residual and NEQSys.evaluate_jac
    """

    tempdir_basename = "_symodesys_compile"


    def __init__(self, neqsys, **kwargs):
        self._neqsys = neqsys
        super(NEQSys_Code, self).__init__(**kwargs)


    def variables(self):
        func_cse_defs, func_new_code = self._get_cse_code(
            self._neqsys.exprs, 'csefunc')

        jac_cse_defs, jac_new_code = self._get_cse_code(
            chain.from_iterable(self._neqsys.jac.tolist()),
            'csefunc')

        return {'func_cse_defs': func_cse_defs,
                'func_new_code': func_new_code,
                'jac_cse_defs': jac_cse_defs,
                'jac_new_code': jac_new_code,
                'NX': self._neqsys.nx}


    def as_arrayified_code(self, expr):
        """
        We want to access variables as elements of arrays..
        """

        # Dummify the expr (to avoid regular expressions to run berserk)
        expr = self._dummify_expr(expr, 'vdummies', self._neqsys.v)
        expr = self._dummify_expr(expr, 'paramdummies', self._neqsys.params)

        # Generate code string
        scode = self.wcode(expr)

        # getitem syntaxify
        scode = self._getitem_syntaxify(scode, 'vdummies', self.v_tok, self.v_offset)
        scode = self._getitem_syntaxify(scode, 'paramdummies', self.param_tok, self.param_offset)

        return scode


class BinarySolver(Solver):

    CodeClass = None

    def __init__(self, **kwargs):
        self.tempdir = kwargs.pop('tempdir', None)
        self.save_temp = kwargs.pop('save_temp', False)
        self.logger = kwargs.pop('logger', None)
        #super(BinarySolver, self).__init__(**kwargs)


    def set_neqsys(self, neqsys):
        super(BinarySolver, self).set_neqsys(neqsys)
        self._binary_mod = None # <-- Clears cache
        self._code = self.CodeClass(
            neqsys = self._neqsys,
            tempdir = self.tempdir,
            save_temp = self.save_temp,
            logger=self.logger,
        )


    def clean(self):
        self._code.clean()


    @property
    def binary_mod(self):
        """
        Returns compiled and imported module.
        Note: lazy caching is employed, set self._binary_mod equal to None to invalidate
        """
        if self._binary_mod == None:
            self._binary_mod = self._code.compile_and_import_binary()
        return self._binary_mod
