from symneqsys.minpack._setup_minpack import f_sources


class MINPACK_Code(NEQSys_Code, F90_Code):

    _copy_files = ['prebuilt/'+x[:-1]+'f' for x in f_sources] +\
                 ['neqsys_wrapper.o']

    _obj_files = [x[:-1]+'f' for x in f_sources] +\
                 ['neqsys_wrapper.o']

    _templates = ['neqsys_template.f90']

    _source_files = ['neqsys.f90']

    _so_file = 'neqsys_wrapper.so'

    extension_name = 'neqsys_wrapper'

    v_tok = 'y'
    v_offset = 1

    param_tok = 'y'
    @property
    def param_offset(self):
        return 1 + self._neqsys.nx

    def __init__(self, *args, **kwargs):
        self._basedir = os.path.dirname(__file__)
        super(MINPACK_Code, self).__init__(*args, **kwargs)
