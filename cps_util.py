"""
cps_util.py
(c) 2013 Pierre Talbot
"""

def cps_foldl_impl(cps_op, cps_end, accu, g):
  try:
    cps_op(accu, g.next(), lambda acc:
      cps_foldl_impl(cps_op, cps_end, acc, g))
  except StopIteration:
    cps_end(accu)

def cps_foldl(cps_op, cps_end, accu, l):
  cps_foldl_impl(cps_op, cps_end, accu, l.__iter__())
