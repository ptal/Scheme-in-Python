This is a simple Scheme interpreter written in Python.  There is also a [blog series detailing the development of this interpreter](http://nickzarr.com/blog4/series/scheme-in-python/).

The Scheme in Python project is a port of the [Scheme in Scheme](http://nickzarr.com/blog4/series/lispy-in-scheme/) project.  The goal is to implement a small subset of Scheme as an interpreter written in Python.

There are a number of goals for this project.  First, implementing Scheme in Scheme allowed us to "cheat" a bit by having access to the Scheme reader and data structures.  Using Python as the implementation language will force us to code the reader by hand and create new data structures where there isn't a one-to-one mapping from Scheme to Python.

There are also two auxiliary goals to this project.  Using Python should make this more accessible to programmers who are interested in language development, but are unfamiliar with Scheme.  Also I'm using this project as a way to familiarize myself with branching and merging in git, so each post will correspond to a branch in the repository.

All the code for this project will be hosted on GitHub.  The code is licensed under a BSD license if you are interested in forking it for any reason.  

This series will focus on building a very simple interpreter for the purpose of learning the steps involved in building one.  For this reason there will be no/very little error checking or optimization.  This port will be slightly more complicated than Scheme in Scheme so if you are interested in an even simpler interpreter look [here](http://nickzarr.com/blog4/series/lispy-in-scheme/).

With that out of the way, here's an example session:

    $ python repl.py
    > (set! two 3)
     Error:  Unbound symbol: two
    > (define two 2)
     
    > (define two (+ 1 2))
     
    > two
     ;===> 3
    > (set! two 2)
     
    > two
     ;===> 2
    > (define add5 (lambda (v) (+ 5 v)))

    > (add5 6)
     ;===> 11
    > (define add (lambda (u v) (+ u v)))
     
    > (add (* 4 3) (/ 4 2))
     ;===> 14
    > (call/cc (lambda (k) (k 5)))
     ;===> 5
    > (- (call/cc (lambda (k) (k two))) 3)
     ;===> -1
    > (call/cc (lambda (k v) (k (+ 5 v))))
     Error:  call/cc only takes a procedure of arity 1.
    > (define inc (lambda () (define j 0) (set! j (+ j 1)) j))
     
    > (inc)
     ;===> 1
    > (inc)
     ;===> 1
    > (exit)

    $ 


(c) 2011 Nick Zarczynski

The initial project (v.10) has been extended by Pierre Talbot and passed the interpreter in Continuation Passing Style (CPS). He also adds the call/cc operation.

(c) 2013 Pierre Talbot

License: BSD
