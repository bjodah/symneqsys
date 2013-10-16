import os
from pycompilation import pyx2obj, c2obj

def main(cwd, logger):
    # Cythonize pyx file
    src = 'solvers_wrapper.pyx'
    dst = 'prebuilt/solvers_wrapper.o'
    pyx2obj(src, dst, cwd=cwd, logger=logger, only_update=True, metadir='prebuilt/')

    f = '_solvers.c'
    fpath = os.path.join(cwd, f)
    dst = 'prebuilt/_solvers.o'
    c2obj(fpath, objpath=dst, flags=['-DGSL_RANGE_CHECK_OFF', '-DHAVE_INLINE'],
          libs=['gsl', 'gslcblas', 'm'], cwd=cwd, metadir='prebuilt/', logger=logger, only_update=True)
    # if missing_or_other_newer(dst, f):
    #     runner = CCompilerRunner(
    #         [fpath], dst, run_linker=False,
    #         flags=['-DGSL_RANGE_CHECK_OFF', '-DHAVE_INLINE'],
    #         cwd=cwd, options=['pic', 'warn', 'fast', 'c99'],
    #         preferred_vendor='gnu', metadir='prebuilt/',
    #         logger=logger)
    #     os.unlink(dst) # make sure failed compilation kills the party..
    #     runner.run()
    # else:
    #     logger.info("{} newer than {}, did not recompile.".format(dst, fpath))
