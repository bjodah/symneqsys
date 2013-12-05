import os
from pycompilation import pyx2obj, src2obj

def main(dst, **kwargs):
    return [
        pyx2obj(
            'solvers_wrapper.pyx',
            dst,
            only_update=True, metadir=dst,
            **kwargs),
        src2obj(
            '_solvers.c',
            objpath=dst,
            flags=['-DGSL_RANGE_CHECK_OFF', '-DHAVE_INLINE'],
            options=['pic', 'warn', 'fast'],
            std='c99',
            libs=['gsl', 'gslcblas', 'm'],
            metadir=dst,
            only_update=True,
            **kwargs)
    ]
