# -*- coding: utf-8 -*-

import os
from pycodeexport.codeexport import make_PCEExtension_for_prebuilding_Code

"""
Precompiles NLEQ2 sources (downloaded when needed) to object files
for speeding up compilations further ahead.

TODO: add a confirmation step where the user accepts the ZIB license.
"""

src_md5 = {
    'linalg_nleq2.f': '28ed88f1ae7bab8dc850348b5e734881',
    'nleq2.f':        '73401c84c8e0d434fffa6f303ba813e0',
    'wnorm.f':        '77189300200be5748152fa28dc236963',
    'zibmon.f':       'e2ac1a20fc6294cb3e0d7f65bbac53e6',
    #'zibconst.f':     '5d912441fb6f55d10c8b98bbb9168195', # in template
    #'zibsec.f':       '6520c958f2bd339b435a68541d5b910b', # in template
} # July 26, 2010 version

f_sources = src_md5.keys()

websrc='http://elib.zib.de/pub/elib/codelib/nleq2/'

def get_nleq2_pce_ext(basename):
    from .interface import NLEQ2_Code
    return make_PCEExtension_for_prebuilding_Code(
        basename+'.nleq2._solvers', NLEQ2_Code,
        f_sources+['_solvers.pyx'],
        srcdir=os.path.join(basename, 'nleq2'),
        downloads=(websrc, src_md5),
        logger=True
    )
