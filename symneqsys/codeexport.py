class NEQSys_Code(Generic_Code):
    """
    Wraps some sympy functionality of code generation from matrices
    returned by NEQSys.evaluate_residual and NEQSys.evaluate_jac
    """

    tempdir_basename = "_symodesys_compile"


    def __init__(self, fo_odesys, **kwargs):
        self._neqsys = neqsys
        super(NEQSys_Code, self).__init__(**kwargs)



class BinarySolver(Solver):

    CodeClass = None

    def __init__(self, **kwargs):
        self.tempdir = kwargs.pop('tempdir', None)
        self.save_temp = kwargs.pop('save_temp', False)
        self.logger = kwargs.pop('logger', None)
        super(BinarySolver, self).__init__(**kwargs)


    def set_fo_odesys(self, fo_odesys):
        super(Binary_IVP_Integrator, self).set_fo_odesys(fo_odesys)
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
