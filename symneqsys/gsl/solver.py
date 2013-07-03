import os

import numpy as np
import cython_gsl

from pycompilation import CCompilerRunner
from pycompilation.codeexport import C_Code


from symneqsys.codeexport import BinarySolver, NEQSys_Code


class GSL_Code(NEQSys_Code, C_Code):

    _copy_files = ['solvers.c',
                   'prebuilt/solvers_wrapper.o',
                   'prebuilt/solvers.o',
                   'solvers.h', 'neqsys.h', 'Makefile',
                   'prebuilt/'+CCompilerRunner.metadata_filename, # <--- Make sure we compile with same compiler
               ]

    _obj_files = ['neqsys.o', 'solvers.o', 'solvers_wrapper.o']

    _templates = ['neqsys_template.c',
                 'main_ex_template.c',
              ]

    _source_files = ['neqsys.c'] # other are precompiled

    _so_file = 'solvers_wrapper.so'

    extension_name = 'solvers_wrapper'


    v_tok = 'y' # see neqsys_template.c
    v_offset = None

    param_tok = 'k' # see neqsys_template.c
    param_offset = None


    def __init__(self, *args, **kwargs):
        self._basedir = os.path.dirname(__file__)
        super(GSL_Code, self).__init__(*args, **kwargs)
        self._include_dirs.append(cython_gsl.get_include())
        self._include_dirs.append(cython_gsl.get_cython_include_dir())
        self._libraries.extend(cython_gsl.get_libraries())
        self._library_dirs.append(cython_gsl.get_library_dir())



class GSL_Solver(BinarySolver):

    CodeClass = GSL_Code

    solve_args = {'fdfsolver_type': (
        'newton', 'gnewton', 'hybridj', 'hybridsj'),
                  }


    def run(self, x0, params, itermax=100, **kwargs):

        for k,v in kwargs.items():
            # Assert valid option provided
            if k in self.solve_args:
                assert v in self.solve_args[k]

        status, x_arr = self.binary_mod.solve(#np.array(x0, dtype=np.float64), np.array(params, dtype=np.float64)
            x0, params, self._atol,
            itermax=itermax, **kwargs)

        self.num_result = Result({
            'x': x_arr,
            'success': status == 0,
            'status': status,
            'message': 'See gsl_errno.h',
            'fun': self.binary_mod.residuals(
                x_arr, params),
            'jac': self.binary_mod.jac(
                x_arr, params),
            # 'nfev': ,
            # 'njev': ,
            # 'nit': ,
            })


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
