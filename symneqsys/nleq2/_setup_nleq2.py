#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Precompiles NLEQ2 sources (downloaded when needed) to object files
for speeding up compilations further ahead.

TODO: add a confirmation step where the user accepts the ZIB license.
"""


def main(cwd, main):
    return
    websrc='http://elib.zib.de/pub/elib/codelib/nleq2/'
    files=['nleq2.f', 'wnorm.f', 'linalg_nleq2.f', 'zibconst.f', 'zibsec.f', 'zibmon.f']
    md5sums= {'linalg_nleq2.f': '28ed88f1ae7bab8dc850348b5e734881',
              'nleq2.f':        '73401c84c8e0d434fffa6f303ba813e0',
              'wnorm.f':        '77189300200be5748152fa28dc236963',
              'zibmon.f':       'e2ac1a20fc6294cb3e0d7f65bbac53e6',
    #          'zibconst.f':     '5d912441fb6f55d10c8b98bbb9168195', # in template
    #          'zibsec.f':       '6520c958f2bd339b435a68541d5b910b', # in template
          } # July 26, 2010 version


    download_files(websrc, files, cwd, md5sums)
    # Intel Fortran fails for opkda1.f, hence prefer `gnu`
    compile_sources(FortranCompilerRunner, files, 'prebuilt/',
                    cwd=cwd, run_linker=False,
                    cwd=cwd, options=['pic', 'warn', 'fast'],
                    preferred_vendor='gnu', metadir=dst, logger=logger)

    # Cythonize pyx file, and compile to object file
    src = 'solvers_wrapper.pyx'
    dst = 'prebuilt/solvers_wrapper.o'
    pyx2obj(src, dst, cwd=cwd, logger=logger, only_update=True)
