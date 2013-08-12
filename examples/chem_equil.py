#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

"""
Example of a 4 dimensional root finidng problem (chemical
acid/base equilbria)
"""

from symneqsys import SimpleNEQSys, Problem
from symneqsys.minpack import MINPACK_Solver

class ChemSys(SimpleNEQSys):
    var_tokens = 'NH3 NH4p Hp OHm H2O'
    param_tokens = 'Kw Ka ' + ' '.join(['init_'+x for x \
                                        in var_tokens.split()])
    @property
    def exprs(self):
        NH3, NH4p, Hp, OHm, H2O, Kw, Ka = [self[token] for token \
                                      in ('NH3', 'NH4p', 'Hp', 'OHm', 'H2O', 'Kw', 'Ka')]
        init = {x: self['init_'+x] for x in self.var_tokens.split()}
        return [Hp*NH3/NH4p-Ka, # Ammonium ion acid equilibrium
                Hp*OHm/H2O-Kw, # Water autoprotolysis equilibrium
                NH3+NH4p-init['NH3']-init['NH4p'], # preservation of N atoms
                3*NH3+4*NH4p+Hp+OHm+2*H2O-(3*init['NH3']+4*init['NH4p']+\
                                           init['Hp']+init['OHm']+2*init['H2O']), # preservation of H atoms
                OHm+H2O-init['OHm']-init['H2O'], # preservation of O atoms
                NH4p+Hp-OHm-(init['NH4p']+init['Hp']-init['OHm']) # preservation of charge
        ]


def main(Sys):
    """
    Solve the example system using Levenberg-Marquardt algorithm
    from Netlib's MINPACK fortran code.
    """

    sys = Sys()
    solver=MINPACK_Solver(save_temp=True, tempdir='./build/chem_equil')
    solver.abstol = 1e-8
    params = {'Kw':1e-14, 'Ka':10**-9.26}
    init = {'NH3': 1e-3, 'NH4p': 0.0, 'Hp': 1e-7,
            'OHm': 1e-7, 'H2O': 1.0}
    params.update({'init_'+key: val for key,val in init.iteritems()})
    problem = Problem(sys, params, guess=init, solver=solver)
    success = problem.solve(itermax=100, solver_type='lm')

    if success:
        print("Successfully found a root: "+\
              ", ".join([key+'='+str(problem.solution[sys[key]]) for key in init.keys()])+\
              ", using Levenberg-Marquard (lm)")
    else:
        print("Root-finding unsuccessful.")
    print('Full numerical info:', problem.solver.num_result)


if __name__ == '__main__':
    main(ChemSys)
