""" larn/savelev.py

This module defines the saved-level I/O functions.

"""

from aghast.util import export, static

from .larncons import *
from .larndata import *
from .larnfunc import *

# FIXME: The C arrays can switch betwen [][] and [], but python cannot.
# I need to rewrite these to put the arrays in the right shape.
# Maybe make cell a 3-d array? (level, x, y)

@export
def savelevel() -> None:
    """ Save the present level into storage """

    pcel: int = level * MAXX * MAXY
    """ Pointer to this level's cells """
    pecel: int = pcel + MAXX * MAXY
    """ Pointer to past end of this level's cells """

    #while pcel < pecel:
    for x in range(MAXX):
        for y in range(MAXY):
            the_cell = cell[pcel]
            pcel += 1

            the_cell.mitem = mitem[x][y]
            the_cell.hitp = hitp[x][y]
            the_cell.item = item[x][y]
            the_cell.know = know[x][y]
            the_cell.iarg = iarg[x][y]


@export
def getlevel() -> None:
    """ Restore a level from storage. """

    pcel: int = level * MAXX * MAXY
    """ Pointer to this level's cells """

    pecel: int = pcel + MAXX * MAXY
    """ Pointer to past end of this level's cells """
	
    #while pcel < pecel:
    for x in range(MAXX):
        for y in range(MAXY):
            the_cell = cell[pcel]
            pcel += 1

            mitem[x][y] = the_cell.mitem
            hitp[x][y] = the_cell.hitp
            item[x][y] = the_cell.item
            know[x][y] = the_cell.know
            iarg[x][y] = the_cell.iarg
