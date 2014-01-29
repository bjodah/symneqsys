# -*- coding: utf-8 -*-
import os

import numpy as np
import cython_gsl

from pycompilation import CCompilerRunner
from pycompilation.codeexport import C_Code


from symneqsys.codeexport import BinarySolver, NEQSys_Code


class GSL_Code(NEQSys_Code, C_Code):

    build_files = [
        'solvers.c',
        'prebuilt/solvers.o',
        'prebuilt/_solvers.o',
        'solvers.h', 'neqsys.h', 'Makefile',
    ]

    obj_files = ['neqsys.o', 'solvers.o', '_solvers.o']

    templates = ['neqsys_template.c',
                 'main_ex_template.c',
              ]

    source_files = ['neqsys.c'] # other are precompiled

    so_file = '_solvers.so'

    extension_name = 'solvers'

    compile_kwargs = {
        'std': 'c99',
        'options': ['fast', 'warn', 'pic'],
        'defmacros': ['GSL_RANGE_CHECK_OFF', 'HAVE_INLINE'],
        'libs': cython_gsl.get_libraries(),
        'inc_dirs': [cython_gsl.get_include(), cython_gsl.get_cython_include_dir()],
        'lib_dirs': [cython_gsl.get_library_dir()]
    }

    v_tok = 'y' # see neqsys_template.c
    v_offset = None

    param_tok = 'k' # see neqsys_template.c
    param_offset = None


    def __init__(self, *args, **kwargs):
        self._basedir = os.path.dirname(__file__)
        super(GSL_Code, self).__init__(*args, **kwargs)


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
