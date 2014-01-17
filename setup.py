#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import tempfile

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
    sub_pkgs = []
else:

    from pycompilation.util import make_dirs
    from symneqsys.nleq2._setup_nleq2 import prebuild as nleq2_prebuild
    from symneqsys.gsl._setup_gsl import prebuild as gsl_prebuild
    from symneqsys.minpack._setup_minpack import prebuild as minpack_prebuild

    sub_folders = ['nleq2', 'gsl', 'minpack']
    prebuilds = zip(sub_folders,
                [nleq2_prebuild, gsl_prebuild, minpack_prebuild])
    sub_pkgs = ['symneqsys.' + x for x in sub_folders]

    def run_prebuilds(build_lib, build_temp):
        """
        Precompile some sources to object files
        and store in `prebuilt/` directories for
        speeding up meta-programming compilations.
        """
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        for name, cb in prebuilds:
            destdir = os.path.join(build_lib, pkg_name, name)
            prebuilt_destdir = os.path.join(destdir, 'prebuilt')
            if not os.path.exists(prebuilt_destdir): make_dirs(prebuilt_destdir)
            srcdir = os.path.join(os.path.dirname(__file__), pkg_name, name)
            cb(srcdir, destdir, build_temp, logger=logger)

    from distutils.command.build_py import build_py as _build_py
    from distutils.core import setup

    class build_py(_build_py):
        """Specialized Python source builder."""
        def run(self):
            if not self.dry_run:
                build_temp = tempfile.mkdtemp('build_temp')
                try:
                    run_prebuilds(self.build_lib, build_temp)
                finally:
                    shutil.rmtree(build_temp)
            _build_py.run(self)

    cmdclass_ = {'build_py': build_py}

setup(
    name=pkg_name,
    version=version_,
    author='Björn Dahlgren',
    author_email='bjodah@DELETEMEgmail.com',
    description='Convenience functions for use with sympy.',
    license = "BSD",
    url='https://github.com/bjodah/'+pkg_name,
    download_url='https://github.com/bjodah/'+pkg_name+'/archive/v'+version_+'.tar.gz',
    packages=['symneqsys'] + sub_pkgs,
    # package_data={pkg_name: [
    #     'symneqsys/'
    # ]}
    cmdclass = cmdclass_,
    classifiers = classifiers
)
