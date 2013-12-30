"""
scheme_eval.py
(c) 2011 Nick Zarczynski
(c) 2013 Pierre Talbot

For most code you should import this as: 
from scheme_eval import scheme_eval
"""

from cps_functional import cps_foldl
from scheme_types import Symbol, Pair, Primitive, the_empty_list, The_Empty_List, Procedure
from buffered_input import Buff
from scheme_read import scheme_read

# Error continuation

def error(msg):
  print msg

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

def set_symbol(symbol, val, env, cont):
  """Set the binding (symbol, val) in the current frame of env"""
  current_environment(env)[symbol] = val
  cont(None)

def lookup_and_set_symbol(symbol, val, environment, cont):  
  """Set the binding (symbol, val) in the environment, the symbol must
     be defined first."""
  env = environment
  while env != the_empty_list:
    if symbol in current_environment(env):
      set_symbol(symbol, val, env)
      cont(current_environment(env)[symbol])
    else:
      env = enclosing_environment(env)
  error("Error: Unbound symbol: " + symbol)

def lookup_symbol_value(symbol, environment, cont):
  """Return the value of symbol or Unbound Symbol error"""
  env = environment
  while env != the_empty_list:
    if symbol in current_environment(env):
      cont(current_environment(env)[symbol])
    else:
      env = enclosing_environment(env)
  error("Error: Unbound symbol: " + symbol)

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
    lookup_symbol_value(expr, env, cont)
  elif type(expr) is Pair:
    if expr.car in special_forms:
      special_forms[expr.car](expr.cdr, env, cont)
    else:
      scheme_eval(expr.car, env, 
        lambda x:
          scheme_apply(x, expr.cdr, env, cont)
      )
  else:
    error("scheme_eval: not implemented")

def append_and_return (accu, e):
  accu.append(e)
  return accu

def make_append_arg(env):
  def append_arg(accu, arg, cont):
    scheme_eval(arg, env, 
      lambda arg_eval: cont(append_and_return(accu, arg_eval)))
  return append_arg

def make_args_list(args, env, cont):
  cps_foldl(make_append_arg(env), cont, [], args)

def primitive_apply(fn, args, env, cont):
  make_args_list(args, env, 
    lambda args: cont(fn(*args))) # unpack arguments.

def eval_sequence(seq, env, cont):
  def eval_instruction(accu, instruct, k):
    scheme_eval(instruct, env,
      lambda inst_eval: k(inst_eval))
  cps_foldl(eval_instruction, cont, None, seq)

def procedure_apply(proc, params, env, cont):
  make_args_list(params, env,
    lambda args:
      eval_sequence(proc.body, 
        extend_environment(dict(zip(proc.parameters, args)), proc.environment), 
        cont))

def callcc_apply(proc, env, cont):
  if type(proc) is Procedure and len(list(proc.parameters)) == 1:
    eval_sequence(proc.body,
      extend_environment(dict({proc.parameters.car: Primitive(cont)}), proc.environment),
      lambda x: None)
  else:
    error("call/cc only takes a procedure of arity 1.")

def scheme_apply(proc, args, env, cont):
  if type(proc) is Primitive:
    primitive_apply(proc.fn, args, env, cont)
  elif type(proc) is Procedure:
    procedure_apply(proc, args, env, cont)
  else:
    error("Error: Undefined procedure")

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
