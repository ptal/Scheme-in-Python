#!/usr/bin/env python
"""
repl.py
(c) 2011 Nick Zarczynski
(c) 2013 Pierre Talbot
License: BSD

A simple repl
"""

import sys
from scheme_read import scheme_read
from scheme_eval import scheme_eval, special_forms, global_environment
from scheme_types import Pair
from buffered_input import Buff

# special_forms['load'](Pair("syntax.scm", None), global_environment, None)

def print_eval_result(inp):
  if inp != None:
    print ';===>', inp
  else:
    print ''

while True:
  print '> ',
  scheme_eval(scheme_read(Buff(sys.stdin)), global_environment, print_eval_result)
