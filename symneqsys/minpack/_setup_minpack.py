# -*- coding: utf-8 -*-

import os
from pycodeexport.codeexport import make_PCEExtension_for_prebuilding_Code


"""
Precompiles Levenberg Marquardt sources of netlib/minpack (downloaded
when needed) to object files for speeding up compilations further ahead.
"""

websrc = 'http://www.netlib.org/minpack/'
src_md5 = {
    'dpmpar.f': '290b5ab2f116903e49c8f542d7afbac6',
    'enorm.f': 'a63a84008c57c577e03b7d892b964bd5',
    'lmder.f': 'c85d3371f3d1da5087d23a10a8b96759',
    'lmder1.f': 'cefb0d9c5ad109912e99a868e63bea49',
    'lmpar.f': '8ed1e10412c27be1f2490ba0f37a1f7b',
    'qrfac.f': 'fc1df4af782730f0fa5110dec34d4e6b',
    'qrsolv.f': 'a74ea0548499e332f79b0226c6ae83b8',
}

f_sources = src_md5.keys()


def get_minpack_pce_ext(basename):
    from .interface import MINPACK_Code
    return make_PCEExtension_for_prebuilding_Code(
        basename+'.minpack._solvers', MINPACK_Code,
        f_sources+['_solvers.pyx'],
        srcdir=os.path.join(basename, 'minpack'),
        downloads=(websrc, src_md5),
        logger=True
    )
