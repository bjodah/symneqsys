# -*- coding: utf-8 -*-

import os
from pycodeexport.codeexport import make_PCEExtension_for_prebuilding_Code

def get_gsl_pce_ext(basename):
    from .interface import GSL_Code
    return make_PCEExtension_for_prebuilding_Code(
        basename+'.gsl._solvers', GSL_Code,
        ['solvers.c', '_solvers.pyx'],
        srcdir=os.path.join(basename, 'gsl'),
        logger=True
    )
