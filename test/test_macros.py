""" Test the macros provided in larnfunc
"""
import textwrap

import larn

def test_exported_names():
    funcnames = textwrap.dedent("""\
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
    """).splitlines()

    for name in funcnames:
        assert name in dir(larn)
