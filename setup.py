import os
import logging

from pycompilation.util import run_sub_setup

from symneqsys.nleq2._setup_nleq2 import main as nleq2_main
from symneqsys.gsl._setup_gsl import main as gsl_main
from symneqsys.minpack._setup_minpack import main as minpack_main

def main():
    """
    Precompile some sources to object files
    and store in `prebuilt/` directories for
    speeding up meta-programming compilations.
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # NLEQ2
    cwd = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
                       './symneqsys/nleq2/')
    run_sub_setup(nleq2_main, 'prebuilt', cwd=cwd, logger=logger)

    # GSL
    cwd = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
                       './symneqsys/gsl/')
    run_sub_setup(gsl_main, 'prebuilt', cwd=cwd, logger=logger)

    # MINPACK
    cwd = os.path.join(os.path.abspath(
        os.path.dirname(__file__)),
                       './symneqsys/minpack/')
    run_sub_setup(minpack_main, 'prebuilt', cwd=cwd, logger=logger)


if __name__ == '__main__':
    main()
