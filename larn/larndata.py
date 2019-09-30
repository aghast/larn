""" larn/larndata.py

    Data declarations. (Was larndata.h)

    Larn is copyrighted 1986 by Noah Morgan.
    
"""
from dataclasses import dataclass
from typing import *

from aghast.util import export

from .larncons import *

from .config import *

# Some C-like definitions:
char = int
long = int
short = int
signed_char = int
unsigned_long = int

#
#
# types
#
#

@dataclass
class struct_cel:
    """ this is the structure that holds the entire dungeon specifications"""
    hitp: short = 0
    """ monster's hit points """
    mitem: signed_char = 0
    """ the monster ID """
    item: signed_char = 0
    """ the object's ID """
    iarg: short = 0
    """ the object's argument """
    know: signed_char = 0
    """ have we been here before """


@export
@dataclass
class struct_sphere:
    """ this is the structure for maintaining & moving the spheres of 
        annihilation
    """
    p: Optional['struct_sphere'] = None
    """ Pointer to next structure """
    x: signed_char = 0
    y: signed_char = 0
    lev: signed_char = 0
    """ location of the sphere """
    dir: signed_char = 0
    """ direction sphere is going in """
    lifetime: signed_char = 0
    """ duration of the sphere """

@export
@dataclass
class struct_monst:
    """ 
        Note: the order of these fields is mirrored in data.py. Do not change
        one without the other.
    """
    name: str = ""
    level: signed_char = 0
    armorclass: short = 0
    damage: signed_char = 0
    attack: signed_char = 0
    defense: signed_char = 0
    genocided: signed_char = 0
    intelligence: signed_char = 0
    """ monsters intelligence -- used to choose movement """
    gold: short = 0
    hitpoints: short = 0
    experience: unsigned_long = 0


@export
@dataclass
class struct_itm:
    """ this is the structure definition for the items in the dnd store """
    price: short = 0
    obj: signed_char = 0
    arg: signed_char = 0
    qty: signed_char = 0


#
#
# data declarations
#
#

course: List[signed_char] = []
export('course')
iven: List[signed_char] = []
export('iven')



screen: List[List[signed_char]] = [[0]*MAXY for _ in range(MAXX)]
export('screen')


diroffx: List[short] = []
export('diroffx')
diroffy: List[short] = []
export('diroffy')
ivenarg: List[short] = []
export('ivenarg')
yrepcount: int
export('yrepcount')
wisid: int
export('wisid')
lfd: int
export('lfd')
fd: int = 0             # input file numbers 
export('fd')            # Used in 2 other places, I believe. diag.c and scores.c


dnd_item: List[struct_itm] = []
export('dnd_item')



#/*
# * store.c
# */
lasttime: int = 0
export('lasttime')


#/*
# * tok.c
# */
move_no_pickup: signed_char = 0
export('move_no_pickup')
