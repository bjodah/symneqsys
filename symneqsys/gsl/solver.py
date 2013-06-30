from pycompilation.codeexport import C_Code

from symneqsys.codeexport import BinarySolver, NEQSys_Code


class GSL_Code(NEQSys_Code, C_Code):

    _copy_files = ['solvers.c'
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


    def run(self, x0, params, itermax=100, *kwargs):

        for k,v in kwargs.items():
            # Assert valid option provided
            if k in self.solve_args:
                assert v in self.solve_args[k]

        self.num_result = self.binary_mod.solve(
            self.x0, self.params, self._atol,
            itermax=itermax, **kwargs)
