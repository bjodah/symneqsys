import os
from pycompilation import pyx2obj, src2obj

def main(cwd, logger):
    # Cythonize pyx file
    pyx2obj(
        'solvers_wrapper.pyx',
        'prebuilt/solvers_wrapper.o',
        cwd=cwd, logger=logger, only_update=True,
        metadir='./prebuilt')

    src2obj(
        os.path.join(cwd, '_solvers.c'),
        objpath='prebuilt/_solvers.o',
        flags=['-DGSL_RANGE_CHECK_OFF', '-DHAVE_INLINE'],
        options=['pic', 'warn', 'fast'], std='c99',
        libs=['gsl', 'gslcblas', 'm'], cwd=cwd,
        metadir='./prebuilt',
        logger=logger, only_update=True)
