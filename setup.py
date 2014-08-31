#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from distutils.core import setup

pkg_name = 'symneqsys'

version_ = '0.0.1'

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: C",
    "Programming Language :: Cython",
    "Programming Language :: Fortran",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Compilers",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
]


if '--help'in sys.argv[1:] or sys.argv[1] in (
        '--help-commands', 'egg_info', 'clean', '--version'):
    cmdclass_ = {}
    ext_modules=ext_modules_,
else:
    from pycodeexport import pce_build_ext
    from symneqsys.nleq2._setup_nleq2 import get_nleq2_pce_ext
    from symneqsys.gsl._setup_gsl import get_gsl_pce_ext
    from symneqsys.minpack._setup_minpack import get_minpack_pce_ext
    ext_modules_ = [
        get_nleq2_pce_ext(pkg_name),
        get_gsl_pce_ext(pkg_name),
        get_minpack_pce_ext(pkg_name),
    ]
    cmdclass_ = {'build_ext': pce_build_ext}

setup(
    name=pkg_name,
    version=version_,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    description='Solve non-linear systems of equation by combining CAS and conventional solvers.',
    license = "BSD",
    url='https://github.com/bjodah/'+pkg_name,
    download_url='https://github.com/bjodah/'+pkg_name+'/archive/v'+version_+'.tar.gz',
    packages=['symneqsys'],
    ext_modules=ext_modules_,
    cmdclass = cmdclass_,
    classifiers = classifiers
)
