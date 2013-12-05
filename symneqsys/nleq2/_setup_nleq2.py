#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Precompiles NLEQ2 sources (downloaded when needed) to object files
for speeding up compilations further ahead.

TODO: add a confirmation step where the user accepts the ZIB license.
"""

from pycompilation import FortranCompilerRunner, pyx2obj, compile_sources
from pycompilation.util import download_files

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

def main(dst, **kwargs):
    return

    download_files(websrc, f_sources, src_md5, kwargs.get('cwd','.'))
    return [
        pyx2obj(
            'solvers_wrapper.pyx',
            dst,
            only_update=True,
            metadir=dst,
            **kwargs)
    ] + compile_sources(
        f_sources, destdir=dst,
        run_linker=False, options=['pic', 'warn', 'fast'],
        metadir=dst, **kwargs)
