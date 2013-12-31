Author
======

Pierre Talbot

Project
=======

Implement the call/cc instruction by passing the interpreter in Continuation Passing Style (CPS).

What's done?
============

* Arithmetic primitives (+, -, /, *).
* set! instruction.
*! Interpreter in CPS.
*! call/cc instruction.
* exit instruction.
* A generic and re-usable CPS fold-left function (see cps_functional.py).

Some notes
==========

This interpreter was initially written to be as simple as possible. It's now harder to understand due to the CPS transformation.

It's implemented with the philosophy "compiler as a library", that's why most of the instructions are in the syntax.scm file.

Continuations are represented as Python closures. We don't use a special structure for continuations but this would be doable.

See the README for a demo session.
