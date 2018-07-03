# -*- coding: utf-8 -*-

from symneqsys.codeexport import BinarySolver, NEQSys_Code


class NLEQ2_Code(NEQSys_Code):
    v_tok = 'x'  # see neqsys_template.f90
    v_offset = 1  # fortran

    param_tok = 'k'  # see neqsys_template.f90
    param_offset = 1  # fortran

    compile_kwargs = {}


class NLEQ2_Solver(BinarySolver):
    CodeClass = NLEQ2_Code
