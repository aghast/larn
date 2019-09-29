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

regen_bottom: signed_char = 0
export('regen_bottom')

floorc: char = 0
export('floorc')

wallc: char = 0
export('wallc')
VERSION: signed_char = 0
export('VERSION')
SUBVERSION: signed_char = 0
export('SUBVERSION')
beenhere: List[signed_char] = []
export('beenhere')
cheat: signed_char = 0
export('cheat')
course: List[signed_char] = []
export('course')
item: List[List[signed_char]] = [[0]*MAXY for _ in range(MAXX)]
export('item')
iven: List[signed_char] = []
export('iven')
know: List[List[signed_char]] = [[0]*MAXY for _ in range(MAXX)]
export('know')

aborted: List[char] = []
export('aborted')

classname: List[str] = []
export('classname')

lastmonst: List[char] = []
export('lastmonst')

lpnt: str = ""
export('lpnt')
lpbuf: str = ""
export('lpbuf')
inbuffer: str = ""
export('inbuffer')

level: signed_char = 0
export('level')
mitem: List[List[signed_char]] = [[0]*MAXY for _ in range(MAXX)]
export('mitem')
monstlevel: List[signed_char] = []
export('monstlevel')
nch: List[signed_char] = []
export('nch')
ndgg: List[signed_char] = []
export('ndgg')
nlpts: List[signed_char] = []
export('nlpts')
nomove: signed_char = 0
export('nomove')
nplt: List[signed_char] = []
export('nplt')
nsw: List[signed_char] = []
export('nsw')
potprob: List[signed_char] = []
export('potprob')

monstnamelist: List[char] = []
export('monstnamelist')

levelname: List[str] = []
export('levelname')

objnamelist: List[char] = []
export('objnamelist')

logname: str = ''
export('logname')





predostuff: signed_char = 0
export('predostuff')
restorflag: signed_char = 0
export('restorflag')
scprob: List[signed_char] = []
export('scprob')
screen: List[List[signed_char]] = [[0]*MAXY for _ in range(MAXX)]
export('screen')
sex: signed_char = 0
export('sex')
spelknow: List[signed_char] = []
export('spelknow')

spelmes: List[str] = []
export('spelmes')
speldescript: List[str] = []
export('speldescript')
spelcode: List[str] = []
export('spelcode')



spelname: List[str] = []
export('spelname')


splev: List[signed_char] = []
export('splev')
stealth: List[List[signed_char]] = [[0]*MAXY for _ in range(MAXX)]
export('stealth')
wizard: signed_char = 0
export('wizard')
diroffx: List[short] = []
export('diroffx')
diroffy: List[short] = []
export('diroffy')
hitflag: short
export('hitflag')
hit2flag: short
export('hit2flag')
hit3flag: short
export('hit3flag')
hitp: List[List[short]] = [[0]*MAXY for _ in range(MAXX)]
export('hitp')
iarg: List[List[short]] = [[0]*MAXY for _ in range(MAXX)]
export('iarg')
ivenarg: List[short] = []
export('ivenarg')
lasthx: short
export('lasthx')
lasthy: short
export('lasthy')
lastnum: short
export('lastnum')
lastpx: short
export('lastpx')
lastpy: short = 0
export('lastpy')
oldx: short
export('oldx')
oldy: short
export('oldy')
playerx: short
export('playerx')
playery: short = 0
export('playery')
enable_scroll: int
export('enable_scroll')
yrepcount: int
export('yrepcount')
userid: int
export('userid')
wisid: int
export('wisid')
lfd: int
export('lfd')
fd: int = 0             # input file numbers 
export('fd')            # Used in 2 other places, I believe. diag.c and scores.c

initialtime: long
export('initialtime')
outstanding_taxes: long
export('outstanding_taxes')
skill: List[long] = []
export('skill')
gtime: long
export('gtime')
c: List[long] = []
export('c')
cbak: List[long] = []
export('cbak')
cell: List[struct_cel] = []
export('cell')
spheres: struct_sphere
export('spheres')

monster: List[struct_monst] = []
export('monster')
	
dnd_item: List[struct_itm] = []
export('dnd_item')


#/*
# * data.c
# */
prayed: signed_char = 0
export('prayed')

scrollname: List[List[char]] = [[0]*MAXSCROLLNAME for _ in range(MAXSCROLL+1)]
export('scrollname')
potionname: List[List[char]] = [[0]*MAXPOTIONNAME for _ in range(MAXPOTION+1)]
export('potionname')

objectname: List[str] = []
export('objectname')


spelweird: List[List[signed_char]] = [[0]*SPNUM for _ in range(MAXMONST+8)]
export('spelweird')



#/*
# * main.c
# */
rmst: int = 0
export('rmst')
dropflag: int = 0
export('dropflag')
save_mode: int = 0
export('save_mode')


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
