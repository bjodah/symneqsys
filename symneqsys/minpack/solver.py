import os

from pycompilation.codeexport import F90_Code

from symneqsys.minpack._setup_minpack import f_sources
from symneqsys.codeexport import BinarySolver, NEQSys_Code

class MINPACK_Code(NEQSys_Code, F90_Code):

    _copy_files = ['prebuilt/'+x[:-1]+'o' for x in f_sources] +\
                 ['prebuilt/neqsys_wrapper.o']

    _obj_files = [x[:-1]+'o' for x in f_sources] +\
                 ['neqsys.o', 'neqsys_wrapper.o']

    _templates = ['neqsys_template.f90']

    _source_files = ['neqsys.f90']

    _so_file = 'neqsys_wrapper.so'

    extension_name = 'neqsys_wrapper'

    v_tok = 'x'
    v_offset = 1

    param_tok = 'x'
    @property
    def param_offset(self):
        return 1 + len(self._neqsys.v)

    def __init__(self, *args, **kwargs):
        self._basedir = os.path.dirname(__file__)
        super(MINPACK_Code, self).__init__(*args, **kwargs)


class MINPACK_Solver(BinarySolver):

    CodeClass = MINPACK_Code

    def run(self, x0, params, itermax=100, **kwargs):
        self.num_result = self.binary_mod.solve(
            x0, params, self.abstol,
            itermax=itermax, **kwargs)
