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

def print_eval_result(inp):
  if inp != None:
    print ';===>', inp

special_forms['load'](Pair("syntax.scm", None), global_environment, lambda x: x)

while True:
  print '> ',
  try:
    scheme_eval(scheme_read(Buff(sys.stdin)), global_environment, print_eval_result)
  except Exception as e:
    print 'Error: Unsupported or invalid syntax.'
    print e
