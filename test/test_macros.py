""" Test the macros provided in larnfunc
"""
import textwrap

import larn

funcnames = textwrap.dedent("""
    newscroll
    newpotion
    newleather
    newchain
    newplate
    newdagger
    newsword
    forget
    disappear
    setbold
    resetbold
    setscroll
    resetscroll
    clear
    cltoeoln
    srand
""".strip()).splitlines()

for name in funcnames:
    assert name in globals()


