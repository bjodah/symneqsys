from itertools import chain

from pycompilation.codeexport import Generic_Code, DummyGroup
from symneqsys.solver import Solver

class NEQSys_Code(Generic_Code):
    """
    Wraps some sympy functionality of code generation from matrices
    returned by NEQSys.evaluate_residual and NEQSys.evaluate_jac
    """

    tempdir_basename = "_symneqsys_compile"


    def __init__(self, neqsys, **kwargs):
        self._neqsys = neqsys
        super(NEQSys_Code, self).__init__(**kwargs)


    def variables(self):
        """
        Returns code fragments for (dense) population of vectors
        and matrices.
        """
        dummy_groups = (
            DummyGroup('vdummies', self._neqsys.v, self.v_tok, self.v_offset),
            DummyGroup('paramdummies', self._neqsys.params, self.param_tok, self.param_offset),
            )

        func_cse_defs, func_new_code = self.get_cse_code(
            self._neqsys.exprs, 'cse', dummy_groups)

        jac_cse_defs, jac_new_code = self.get_cse_code(
            chain.from_iterable(self._neqsys.jac.tolist()),
            'cse', dummy_groups)

        fj_cse_defs, fj_new_code = self.get_cse_code(
            chain(self._neqsys.exprs, chain.from_iterable(
                self._neqsys.jac.tolist())), 'cse',
            dummy_groups)

        fj_func_new_code = fj_new_code[:len(self._neqsys.v)]
        fj_jac_new_code = fj_new_code[len(self._neqsys.v):]

        return {'func_cse_defs': func_cse_defs,
                'func_new_code': func_new_code,
                'jac_cse_defs': jac_cse_defs,
                'jac_new_code': jac_new_code,
                'fj_cse_defs': fj_cse_defs,
                'fj_func_new_code': fj_func_new_code,
                'fj_jac_new_code': fj_jac_new_code,
                'NX': len(self._neqsys.v),
                'NE': len(self._neqsys.exprs),
                'NPARAMS': len(self._neqsys.params)}


class BinarySolver(Solver):

    CodeClass = None

    def __init__(self, **kwargs):
        self.tempdir = kwargs.pop('tempdir', None)
        self.save_temp = kwargs.pop('save_temp', False)
        self.logger = kwargs.pop('logger', None)
        if len(kwargs) > 0:
            raise TypeError('{} got (an) unexpected keyword argument(s): {}'.format(
                self, ', '.join(kwargs.keys())))
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

class Result(dict):
    """ Copy from scipy/optimize/optimize.py, cannot import  """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __repr__(self):
        if self.keys():
            m = max(map(len, self.keys())) + 1
            return '\n'.join([k.rjust(m) + ': ' + repr(v)
                              for k, v in self.iteritems()])
        else:
            return self.__class__.__name__ + "()"
