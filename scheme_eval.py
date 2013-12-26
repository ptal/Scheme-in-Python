"""
scheme_eval.py
(c) 2011 Nick Zarczynski
(c) 2013 Pierre Talbot

For most code you should import this as: 
from scheme_eval import scheme_eval
"""

from cps_util import cps_foldl
from scheme_types import Symbol, Pair, Primitive, the_empty_list, The_Empty_List, Procedure
from buffered_input import Buff
from scheme_read import scheme_read

##############################################################################
## Environments
##############################################################################

def current_environment(env):
  """Return the frame of the current environment"""
  return env.car

def enclosing_environment(env):
  """Return the environment stack with the first frame removed"""
  return env.cdr

def extend_environment(bindings, base_environment):
  """Push a new frame onto the given base_environment"""
  return Pair(bindings, base_environment)

global_environment = extend_environment({}, the_empty_list)
special_forms = {}

def set_symbol(symbol, val, env):
  """Set the binding (symbol, val) in the current frame of env"""
  current_environment(env)[symbol] = val

def lookup_symbol_value(symbol, environment):
  """Return the value of symbol or Unbound Symbol error"""
  env = environment
  while env != the_empty_list:
    if symbol in current_environment(env):
      return current_environment(env)[symbol]
    else:
      env = enclosing_environment(env)
  return "Error: Unbound symbol: " + symbol

##############################################################################
## Eval and Apply
##############################################################################

def self_evaluating(expr):
  t = type(expr)
  return t is int or t is float or t is str or t is bool

def scheme_eval(expr, env, cont):
  if self_evaluating(expr):
    cont(expr)
  elif type(expr) is Symbol:
    cont(lookup_symbol_value(expr, env))
  elif type(expr) is Pair:
    if expr.car in special_forms:
      special_forms[expr.car](expr.cdr, env, cont)
    else:
      scheme_eval(expr.car, env, 
        lambda x:
          scheme_apply(x, expr.cdr, env, cont)
      )
  else:
    cont("scheme_eval: not implemented")

def make_append_arg(env):
  def append_arg(accu, arg, cont):
    scheme_eval(arg, env, 
      lambda arg_eval: cont(accu.append(arg_eval)))
  return append_arg

def make_args_list(args, env, cont):
  cps_foldl(make_append_arg(env), cont, [], args)

def primitive_apply(fn, args, env, cont):
  make_args_list(args, env, lambda args:
    cont(fn(*args))) # unpack arguments.

def scheme_apply(proc, args, env, cont):
  if type(proc) is Primitive:
    primitive_apply(proc.fn, args, env, cont)
  # elif type(proc) is Procedure:
    # new_env = extend_environment(dict(zip(proc.parameters, args)), proc.environment)
    # return [scheme_eval(e,new_env) for e in proc.body][-1]
  else:
    cont("Error: Undefined procedure")

##############################################################################
## Builtin Syntax
##############################################################################

def special_form_handler(expr, env, cont):
  """Register a symbol with a Python function named "f" that implements a special form"""
  exec(expr.cdr.car)
  special_forms[expr.car] = f
  cont(None)

def load(expr, env, cont):
  """Given a filename, open it and eval each expression in the global_environment"""
  f = open(expr.car, 'r')
  b = Buff(f)
  while b.peek():
    scheme_eval(scheme_read(b), env, cont)
    b.remove_whitespace()
  f.close()

special_forms['scheme-syntax'] = special_form_handler
special_forms['load'] = load
