import os

import numpy as np
import cython_gsl

from pycompilation import CCompilerRunner
from pycompilation.codeexport import C_Code


from symneqsys.codeexport import BinarySolver, NEQSys_Code


class GSL_Code(NEQSys_Code, C_Code):

    copy_files = [
        '_solvers.c',
        'prebuilt/solvers_wrapper.o',
        'prebuilt/_solvers.o',
        '_solvers.h', 'neqsys.h', 'Makefile',
        # Make sure we compile with same compiler:
        'prebuilt/'+CCompilerRunner.metadata_filename,
    ]

    obj_files = ['neqsys.o', '_solvers.o', 'solvers_wrapper.o']

    templates = ['neqsys_template.c',
                 'main_ex_template.c',
              ]

    source_files = ['neqsys.c'] # other are precompiled

    so_file = 'solvers_wrapper.so'

    extension_name = 'solvers_wrapper'

    compile_kwargs = {
        'std': 'c99',
        'options': ['fast', 'warn', 'pic'],
    }

    v_tok = 'y' # see neqsys_template.c
    v_offset = None

    param_tok = 'k' # see neqsys_template.c
    param_offset = None


    def __init__(self, *args, **kwargs):
        self._basedir = os.path.dirname(__file__)
        super(GSL_Code, self).__init__(*args, **kwargs)
        self.inc_dirs.append(cython_gsl.get_include())
        self.inc_dirs.append(cython_gsl.get_cython_include_dir())
        self.libs.extend(cython_gsl.get_libraries())
        self.lib_dirs.append(cython_gsl.get_library_dir())


class GSL_Solver(BinarySolver):
    """
    Used to solve systems with equal number of expressions
    as variables.
    """
    CodeClass = GSL_Code

    solve_args = {'fdfsolver_type': (
        'newton', 'gnewton', 'hybridj', 'hybridsj'),}

    def run(self, x0, params, itermax=100, **kwargs):
        self.num_result = self.binary_mod.solve(
            x0, params, atol=self.abstol,
            itermax=itermax, **kwargs)


class GSL_Multifit_Nlin_Solver(BinarySolver):
    pass


class GSL_MultiRoot_Solver(BinarySolver):
    pass
