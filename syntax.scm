(scheme-syntax define-primitive "
def f(expr, env, cont):
  set_symbol(expr.car, Primitive(eval(expr.cdr.car)), env)
  cont(None)
")

(scheme-syntax define "
def f(expr, env, cont):
  scheme_eval(expr.cdr.car, env, lambda x:
    set_symbol(expr.car, x, env))
")

(scheme-syntax if "
def f(expr, env, cont):
  scheme_eval(expr.car, env, 
    lambda x:
      scheme_eval(expr.cdr.car, env, cont) if x
      else scheme_eval(expr.cdr.cdr.car, env, cont))
")

(scheme-syntax lambda "
def f(expr, env, cont):
  cont(Procedure(expr.car, expr.cdr, env))
")

(define-primitive + "lambda x, y: x+y")
(define-primitive * "lambda x, y: x*y")
(define-primitive / "lambda x, y: x/y")
(define-primitive - "lambda x, y: x-y")
