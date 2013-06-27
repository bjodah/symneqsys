#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Precompiles Levenberg Marquard sources of netlib/minpack (downloaded when needed) to object files
for speeding up compilations further ahead.
"""

websrc='http://www.netlib.org/minpack/'

files=['dpmpar.f', 'enorm.f', 'lmder.f', 'lmder1.f', 'lmpar.f', 'qrfac.f', 'qrsolv.f']
md5sums= {
    'dpmpar.f': '290b5ab2f116903e49c8f542d7afbac6',
    'enorm.f': 'a63a84008c57c577e03b7d892b964bd5',
    'lmder.f': 'c85d3371f3d1da5087d23a10a8b96759',
    'lmder1.f': 'cefb0d9c5ad109912e99a868e63bea49',
    'lmpar.f': '8ed1e10412c27be1f2490ba0f37a1f7b',
    'qrfac.f': 'fc1df4af782730f0fa5110dec34d4e6b',
    'qrsolv.f': 'a74ea0548499e332f79b0226c6ae83b8',
}


def main():
    pass
