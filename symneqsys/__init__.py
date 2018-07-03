# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)

from .problem import Problem
from .neqsys import NEQSys, SimpleNEQSys

__version__ = '0.0.1'

assert (Problem, NEQSys, SimpleNEQSys)  # silence pyflakes
