""" data.c

    #include "larncons.h"
    #include "larndata.h"
    #include "larnfunc.h"
"""
from typing import (List, Optional)

from .larncons import *
from .larndata import *

VER = 12  # type: int
""" #define VER    12 """
SUBVER = 4  # type: int
""" #define SUBVER  4 """

classname = [
    "  novice explorer  ", "apprentice explorer", " practiced explorer",#  -3
    "   expert explorer ", "  novice adventurer", "     adventurer    ",#  -6
    "apprentice conjurer", "     conjurer      ", "  master conjurer  ",#  -9
    "  apprentice mage  ", "        mage       ", "  experienced mage ",# -12
    "     master mage   ", " apprentice warlord", "   novice warlord  ",# -15
    "   expert warlord  ", "   master warlord  ", " apprentice gorgon ",# -18
    "       gorgon      ", "  practiced gorgon ", "   master gorgon   ",# -21
    "    demi-gorgon    ", "    evil master    ", " great evil master ",# -24
    " mighty evil master", " mighty evil master", " mighty evil master",# -27
    " mighty evil master", " mighty evil master", " mighty evil master",# -30
    " mighty evil master", " mighty evil master", " mighty evil master",# -33
    " mighty evil master", " mighty evil master", " mighty evil master",# -36
    " mighty evil master", " mighty evil master", " mighty evil master",# -39
    "apprentice demi-god", "apprentice demi-god", "apprentice demi-god",# -42
    "apprentice demi-god", "apprentice demi-god", "apprentice demi-god",# -45
    "apprentice demi-god", "apprentice demi-god", "apprentice demi-god",# -48
    "  minor demi-god   ", "  minor demi-god   ", "  minor demi-god   ",# -51
    "  minor demi-god   ", "  minor demi-god   ", "  minor demi-god   ",# -54
    "  minor demi-god   ", "  minor demi-god   ", "  minor demi-god   ",# -57
    "  major demi-god   ", "  major demi-god   ", "  major demi-god   ",# -60
    "  major demi-god   ", "  major demi-god   ", "  major demi-god   ",# -63
    "  major demi-god   ", "  major demi-god   ", "  major demi-god   ",# -66
    "    minor deity    ", "    minor deity    ", "    minor deity    ",# -69
    "    minor deity    ", "    minor deity    ", "    minor deity    ",# -72
    "    minor deity    ", "    minor deity    ", "    minor deity    ",# -75
    "    major deity    ", "    major deity    ", "    major deity    ",# -78
    "    major deity    ", "    major deity    ", "    major deity    ",# -81
    "    major deity    ", "    major deity    ", "    major deity    ",# -84
    "  novice guardian  ", "  novice guardian  ", "  novice guardian  ",# -87
    "apprentice guardian", "apprentice guardian", "apprentice guardian",# -90
    "apprentice guardian", "apprentice guardian", "apprentice guardian",# -93
    "  earth guardian   ", "   air guardian    ", "   fire guardian   ",# -96
    "  water guardian   ", "  time guardian    ", " ethereal guardian ",# -99
    "    The Creator    ", "    The Creator    ", "    The Creator    ",# -102
]  # type: List[str]
""" classname[c[LEVEL]-1] gives the correct name of the players experience level
"""
export('classname')

MEG = 1000000  # type: int
""" #define MEG 1000000 """
skill = [
    0, 10, 20, 40, 80, 160, 320, 640, 1280, 2560, 5120,                 #  1-11 
    10240, 20480, 40960, 100000, 200000, 400000, 700000, 1*MEG,         # 12-19 
    2*MEG,3*MEG,4*MEG,5*MEG,6*MEG,8*MEG,10*MEG,                         # 20-26 
    12*MEG,14*MEG,16*MEG,18*MEG,20*MEG,22*MEG,24*MEG,26*MEG,28*MEG,     # 27-35 
    30*MEG,32*MEG,34*MEG,36*MEG,38*MEG,40*MEG,42*MEG,44*MEG,46*MEG,     # 36-44 
    48*MEG,50*MEG,52*MEG,54*MEG,56*MEG,58*MEG,60*MEG,62*MEG,64*MEG,     # 45-53 
    66*MEG,68*MEG,70*MEG,72*MEG,74*MEG,76*MEG,78*MEG,80*MEG,82*MEG,     # 54-62 
    84*MEG,86*MEG,88*MEG,90*MEG,92*MEG,94*MEG,96*MEG,98*MEG,100*MEG,    # 63-71 
    105*MEG,110*MEG,115*MEG,120*MEG, 125*MEG, 130*MEG, 135*MEG, 140*MEG,# 72-79 
    145*MEG,150*MEG,155*MEG,160*MEG, 165*MEG, 170*MEG, 175*MEG, 180*MEG,# 80-87 
    185*MEG,190*MEG,195*MEG,200*MEG, 210*MEG, 220*MEG, 230*MEG, 240*MEG,# 88-95 
    250*MEG,260*MEG,270*MEG,280*MEG, 290*MEG, 300*MEG                   # 96-101
]  # type: List[int]
""" table of experience needed to be a certain level of player
    skill[c[LEVEL]] is the experience required to attain the next level
"""
export('skill')
    
del MEG
""" #undef MEG """

lpbuf = None  # type: Optional[bytearray]
""" char *lpbuf,*lpnt,*inbuffer,*lpend; /* input/output pointers to the buffers */
"""
export('lpbuf')
lpnt = 0  # type: int
""" char *lpbuf,*lpnt,*inbuffer,*lpend; /* input/output pointers to the buffers */
"""
export('lpnt')
inbuffer = None  # type: Optional[bytearray]
""" char *lpbuf,*lpnt,*inbuffer,*lpend; /* input/output pointers to the buffers */
"""
export('inbuffer')
lpend = 0  # type: int
""" char *lpbuf,*lpnt,*inbuffer,*lpend; /* input/output pointers to the buffers */
"""
export('lpend')
cell = None  # type: Optional[List[struct_cel]]
""" struct cel *cell;   /*  pointer to the dungeon storage  */
"""
export('cell')

hitp = None  # type: Optional[List[List[int]]]
""" short hitp[MAXX][MAXY];     /*  monster hp on level     */
"""
export('hitp')
iarg = None  # type: Optional[List[List[int]]]
""" short iarg[MAXX][MAXY]; /*  arg for the item array  */
"""
export('iarg')
item = None  # type: Optional[List[List[int]]]
""" signed char item[MAXX][MAXY];  /*  objects in maze if any  */
"""
export('item')
know = None  # type: Optional[List[List[int]]]
""" signed char know[MAXX][MAXY];  /*  1 or 0 if here before   */
"""
export('know')
mitem = None  # type: Optional[List[List[int]]]
""" signed char mitem[MAXX][MAXY]; /*  monster item array      */
"""
export('mitem')
stealth = None  # type: Optional[List[List[int]]]
""" signed char stealth[MAXX][MAXY];   /*  0=sleeping 1=awake monst*/
"""
export('stealth')

lastmonst = ""  # type: str
""" char lastmonst[40];     /*  this has the name of the current monster    */
"""
beenhere = [0] * (MAXLEVEL + MAXVLEVEL)  # type: List[int]
""" signed char beenhere[MAXLEVEL+MAXVLEVEL];  /*  1 if have been on this level */
"""
VERSION = VER  # type: int
""" signed char VERSION=VER;   /*  this is the present version # of the program    */
"""
SUBVERSION = SUBVER  # type: int
""" signed char SUBVERSION=SUBVER;
"""
predostuff = 0  # type: int
""" signed char predostuff=0;  /*  2 means that the trap handling routines must do a
                        showplayer() after a trap.  0 means don't showplayer()
                        0 - we are in create player screen
                        1 - we are in welcome screen
                        2 - we are in the normal game   */
"""

logname = ""  # type: str
""" char logname[LOGNAMESIZE];  /* the player's name */
"""


sex = 1  # type: int
""" signed char sex=1;             /*  default is a man  0=woman                       */
"""
cheat = 0  # type: int
""" signed char cheat=0;           /*  1 if the player has fudged save file            */
"""
level = 0  # type: int
""" signed char level=0;           /*  cavelevel player is on = c[CAVELEVEL]           */
"""
wizard = 0  # type: int
""" signed char wizard=0;          /*  the wizard mode flag                            */
"""
lastnum = 0  # type: int
""" short lastnum=0;        /* the number of the monster last hitting player    */
"""
hitflag = 0  # type: int
""" short hitflag=0;        /*  flag for if player has been hit when running    */
"""
hit2flag = 0  # type: int
""" short hit2flag=0;       /*  flag for if player has been hit when running    */
"""
hit3flag = 0  # type: int
""" short hit3flag=0;       /*  flag for if player has been hit flush input     */
"""
playerx = playery = 0  # type: int
""" short playerx,playery;  /*  the room on the present level of the player     */
"""
lastpx = lastpy = 0  # type: int
""" short lastpx,lastpy;    /*  0 --- MAXX-1  or  0 --- MAXY-1                  */
"""
oldx = oldy = 0  # type: int
""" short oldx,oldy;
"""
prayed = 1  # type: int
""" signed char  prayed = 1;       /* did player pray at an altar (command mode)? needs
                           to be saved, but I don't want to add incompatibility
                           right now.  KBR 1/11/90 */
"""
lasthx = lasthy = 0  # type: int
""" short lasthx=0,lasthy=0;/* location of monster last hit by player       */
"""
lrandx = 33601  # type: int
""" unsigned long lrandx=33601;  /*  the random number seed                      */
"""
initialtime = 0  # type: int
""" long initialtime=0;         /* time playing began                           */
"""
gtime = 0  # type: int
""" long gtime=0;               /*  the clock for the game                      */
"""
outstanding_taxes = 0  # type: int
""" long outstanding_taxes=0;   /* present tax bill from score file             */
"""
c = [0] * 100  # type: List[int]
""" long c[100],cbak[100];      /*  the character description arrays            */
"""
cbak = [0] * 100  # type: List[int]
""" long c[100],cbak[100];      /*  the character description arrays            */
"""
enable_scroll = 0  # type: int
""" int enable_scroll=0;        /* constant for enabled/disabled scrolling regn */
"""
aborted = " aborted"  # type: str
""" char aborted[] = " aborted";
"""
spheres = None  # type: Optional[List[None]]
""" struct sphere *spheres=0; /*pointer to linked list for spheres of annihilation*/
"""
levelname = "H 1 2 3 4 5 6 7 8 9 10 V1 V2 V3".split()  # type: List[str]
""" char *levelname[]=
    { " H"," 1"," 2"," 3"," 4"," 5"," 6"," 7"," 8"," 9","10","V1","V2","V3" };
"""


objnamelist = (
    ".:\\_^<_{%^6|2>_55}$'+#~[[[))))))========-?!"
    "?&~~~~~****899)))[[[[[)^.[1$$$.^^.3./0\\4,_________"
).split('')  # type: List[str]
""" char objnamelist[MAXOBJECT+1] = 
        ".:\\_^<_{%^6|2>_55}$'+#~[[[))))))========-?!"
        "?&~~~~~****899)))[[[[[)^.[1$$$.^^.3./0\\4,_________";
"""
assert len(objnamelist) == MAXOBJECT

monstnamelist = (
    ".BGHJKOScjtAELNQRZabhiCTYdegmvzFWflorXV.pqsyUkMwDDPxnDDuD"
    "........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
    ",,,,,,,,,,,,,,"
).split('')  # type: List[str]
""" char monstnamelist[]=".BGHJKOScjtAELNQRZabhiCTYdegmvzFWflorXV.pqsyUkMwDDPxnDDuD........,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,";
"""
assert len(monstnamelist) == MAXMONST

regen_bottom = 0  # type: int
""" extern signed char regen_bottom;
"""
export('regen_bottom')

floorc = '.'  # type: str
""" char floorc = '.';
"""
wallc = '#'  # type: str
""" char wallc  = '#';
"""

objectname = [
    "","a holy altar","a handsome jewel encrusted throne","the orb","a pit",
    "a staircase leading upwards","an elevator going up","a bubbling fountain",
    "a great marble statue","a teleport trap","the college of Larn",
    "a mirror","the DND store","a staircase going down","an elevator going down",
    "the bank of Larn","the 5th branch of the Bank of Larn",
    "a dead fountain","gold","an open door","a closed door",
    "a wall","The Eye of Larn","plate mail","chain mail","leather armor",
    "a sword of slashing","Bessman's flailing hammer","a sunsword",
    "a two handed sword","a spear","a dagger",
    "ring of extra regeneration","a ring of regeneration","a ring of protection",
    "an energy ring","a ring of dexterity","a ring of strength",
    "a ring of cleverness","a ring of increase damage","a belt of striking",
    "a magic scroll","a magic potion","a book","a chest",
    "an amulet of invisibility","an orb of dragon slaying",
    "a scarab of negate spirit","a cube of undead control",
    "device of theft prevention","a brilliant diamond","a ruby",
    "an enchanting emerald","a sparkling sapphire","the dungeon entrance",
    "a volcanic shaft leaning downward","the base of a volcanic shaft",
    "a battle axe","a longsword","a flail","ring mail","studded leather armor",
    "splint mail","plate armor","stainless plate armor","a lance of death",
    "an arrow trap","an arrow trap","a shield","your home",
    "gold","gold","gold","a dart trap",
    "a dart trap","a trapdoor","a trapdoor","the local trading post",
    "a teleport trap", "a massive throne",
    "a sphere of annihilation","a handsome jewel encrusted throne",
    "the Larn Revenue Service","a fortune cookie","","","","","","",
    "","","","","","","","","","","","","","","","","","","",""
]  # type: List[str]
""" char *objectname[]=
    { 0,"a holy altar","a handsome jewel encrusted throne","the orb","a pit",
      "a staircase leading upwards","an elevator going up","a bubbling fountain",
      "a great marble statue","a teleport trap","the college of Larn",
      "a mirror","the DND store","a staircase going down","an elevator going down",
      "the bank of Larn","the 5th branch of the Bank of Larn",
      "a dead fountain","gold","an open door","a closed door",
      "a wall","The Eye of Larn","plate mail","chain mail","leather armor",
      "a sword of slashing","Bessman's flailing hammer","a sunsword",
      "a two handed sword","a spear","a dagger",
      "ring of extra regeneration","a ring of regeneration","a ring of protection",
      "an energy ring","a ring of dexterity","a ring of strength",
      "a ring of cleverness","a ring of increase damage","a belt of striking",
      "a magic scroll","a magic potion","a book","a chest",
      "an amulet of invisibility","an orb of dragon slaying",
      "a scarab of negate spirit","a cube of undead control",
      "device of theft prevention","a brilliant diamond","a ruby",
      "an enchanting emerald","a sparkling sapphire","the dungeon entrance",
      "a volcanic shaft leaning downward","the base of a volcanic shaft",
      "a battle axe","a longsword","a flail","ring mail","studded leather armor",
      "splint mail","plate armor","stainless plate armor","a lance of death",
      "an arrow trap","an arrow trap","a shield","your home",
      "gold","gold","gold","a dart trap",
      "a dart trap","a trapdoor","a trapdoor","the local trading post",
      "a teleport trap", "a massive throne",
      "a sphere of annihilation","a handsome jewel encrusted throne",
      "the Larn Revenue Service","a fortune cookie","","","","","","",
      "","","","","","","","","","","","","","","","","","","",""
     };
"""


monstlevel = [ 
    5, 11, 17, 22, 27, 33, 39, 42, 46, 50, 53, 56, 59 
]  # type: List[int]
""" /*
     *  for the monster data
     *
     *  array to do rnd() to create monsters <= a given level
     */
    signed char monstlevel[] = { 5, 11, 17, 22, 27, 33, 39, 42, 46, 50, 53, 56, 59 };
"""


monster = [struct_monst(*tpl) for tpl in (

# NAME              LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
# ----------------------------------------------------------------- */
( "",               0,  0,  0,  0,  0,   0,  3,   0,    0,  0   ),
( "bat",            1,  0,  1,  0,  0,   0,  3,   0,    1,  1   ),
( "gnome",          1,  10, 1,  0,  0,   0,  8,  30,    2,  2   ),
( "hobgoblin",      1,  14, 2,  0,  0,   0,  5,  25,    3,  2   ),
( "jackal",         1,  17, 1,  0,  0,   0,  4,   0,    1,  1   ),
( "kobold",         1,  20, 1,  0,  0,   0,  7,  10,    1,  1   ),

( "orc",            2,  12, 1,  0,  0,   0,  9,  40,    4,  2   ),
( "snake",          2,  15, 1,  0,  0,   0,  3,   0,    3,  1   ),
( "giant centipede",2,  14, 0,  4,  0,   0,  3,   0,    1,  2   ),
( "jaculi",         2,  20, 1,  0,  0,   0,  3,   0,    2,  1   ),
( "troglodyte",     2,  10, 2,  0,  0,   0,  5,  80,    4,  3   ),
( "giant ant",      2,  8,  1,  4,  0,   0,  4,   0,    5,  5   ),

# NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
# ----------------------------------------------------------------- */
( "floating eye",   3,  8,  1,  0,  0,   0,  3,   0,     5,  2  ),
( "leprechaun",     3,  3,  0,  8,  0,   0,  3,1500,    13, 45  ),
( "nymph",          3,  3,  0,  14, 0,   0,  9,   0,    18, 45  ),
( "quasit",         3,  5,  3,  0,  0,   0,  3,   0,    10, 15  ),
( "rust monster",   3,  4,  0,  1,  0,   0,  3,   0,    18, 25  ),
( "zombie",         3,  12, 2,  0,  0,   0,  3,   0,     6,  7  ),

( "assassin bug",   4,  9,  3,  0,  0,   0,  3,   0,    20, 15  ),
( "bugbear",        4,  5,  4,  15, 0,   0,  5,  40,    20, 35  ),
( "hell hound",     4,  5,  2,  2,  0,   0,  6,   0,    16, 35  ),
( "ice lizard",     4,  11, 2,  10, 0,   0,  6,  50,    16, 25  ),
( "centaur",        4,  6,  4,  0,  0,   0, 10,  40,    24, 45  ),

#   NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
# --------------------------------------------------------------- */
( "troll",          5,  4,  5,  0,  0,   0,  9,  80,    50, 300 ),
( "yeti",           5,  6,  4,  0,  0,   0,  5,  50,    35, 100 ),
( "white dragon",   5,  2,  4,  5,  0,   0, 16, 500,    55, 1000),
( "elf",            5,  8,  1,  0,  0,   0, 15,  50,    22, 35  ),
( "gelatinous cube",5,  9,  1,  0,  0,   0,  3,   0,    22, 45  ),

( "metamorph",      6,  7,  3,  0,  0,   0,  3,  0,     30, 40  ),
( "vortex",         6,  4,  3,  0,  0,   0,  3,  0,     30, 55  ),
( "ziller",         6,  15, 3,  0,  0,   0,  3,  0,     30, 35  ),
( "violet fungi",   6,  12, 3,  0,  0,   0,  3,  0,     38, 100 ),
( "wraith",         6,  3,  1,  6,  0,   0,  3,  0,     30, 325 ),
( "forvalaka",      6,  2,  5,  0,  0,   0,  7,  0,     50, 280 ),

#   NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
# --------------------------------------------------------------- */
( "lama nobe",      7,  7,  3,  0,  0,   0,  6,  0,     35, 80  ),
( "osequip",        7,  4,  3,  16, 0,   0,  4,  0,     35, 100 ),
( "rothe",          7,  15, 5,  0,  0,   0,  3,  100,   50, 250 ),
( "xorn",           7,  0,  6,  0,  0,   0, 13,  0,     60, 300 ),
( "vampire",        7,  3,  4,  6,  0,   0, 17,  0,     50, 1000),
( "invisible stalker",7,3,  6,  0,  0,   0,  5,  0,     50, 350 ),

( "poltergeist",    8,  1,  4,  0,  0,   0,  3,  0,     50, 450 ),
( "disenchantress", 8,  3,  0,  9,  0,   0,  3,  0,     50, 500 ),
( "shambling mound",8,  2,  5,  0,  0,   0,  6,  0,     45, 400 ),
( "yellow mold",    8,  12, 4,  0,  0,   0,  3,  0,     35, 250 ),
( "umber hulk",     8,  3,  7,  11, 0,   0, 14,  0,     65, 600 ),
#   NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
# --------------------------------------------------------------- */

( "gnome king",     9,  -1, 10, 0,  0,   0, 18,  2000,  100,3000    ),
( "mimic",          9,   5, 6,  0,  0,   0,  8,  0,     55, 99      ),
( "water lord",     9, -10, 15, 7,  0,   0, 20,  0,     150,15000   ),
( "bronze dragon",  9,   2, 9,  3,  0,   0, 16,  300,   80, 4000    ),
( "green dragon",   9,   3, 8,  10, 0,   0, 15,  200,   70, 2500    ),
( "purple worm",    9,  -1, 11, 0,  0,   0,  3,  100,   120,15000   ),
( "xvart",          9,  -2, 12, 0,  0,   0, 13,  0,     90, 1000    ),

( "spirit naga",    10, -20,12, 12, 0,   0, 23,  0,     95, 20000   ),
( "silver dragon",  10, -1, 12, 3,  0,   0, 20,  700,   100,10000   ),
( "platinum dragon",10, -5, 15, 13, 0,   0, 22,  1000,  130,24000   ),
( "green urchin",   10, -3, 12, 0,  0,   0,  3,  0,     85, 5000    ),
( "red dragon",     10, -2, 13, 3,  0,   0, 19,  800,   110,14000   ),

( "type I demon lord",  12,-30, 18, 0,   0,  0, 20, 0,  140,50000   ),
( "type II demon lord", 13,-30, 18, 0,   0,  0, 21, 0,  160,75000   ),
( "type III demon lord",14,-30, 18, 0,   0,  0, 22, 0,  180,100000  ),
( "type IV demon lord", 15,-35, 20, 0,   0,  0, 23, 0,  200,125000  ),
( "type V demon lord",  16,-40, 22, 0,   0,  0, 24, 0,  220,150000  ),
( "type VI demon lord", 17,-45, 24, 0,   0,  0, 25, 0,  240,175000  ),
( "type VII demon lord",18,-70, 27, 6,   0,  0, 26, 0,  260,200000  ),
( "demon prince",       25,-127,30, 6,   0,  0, 28, 0,  345,300000  )
)]  # type: List[struct_monst]
""" struct monst monster[] = {
    /*  NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
    ----------------------------------------------------------------- */
    { "",               0,  0,  0,  0,  0,   0,  3,   0,    0,  0   },
    { "bat",            1,  0,  1,  0,  0,   0,  3,   0,    1,  1   },
    { "gnome",          1,  10, 1,  0,  0,   0,  8,  30,    2,  2   },
    { "hobgoblin",      1,  14, 2,  0,  0,   0,  5,  25,    3,  2   },
    { "jackal",         1,  17, 1,  0,  0,   0,  4,   0,    1,  1   },
    { "kobold",         1,  20, 1,  0,  0,   0,  7,  10,    1,  1   },

    { "orc",            2,  12, 1,  0,  0,   0,  9,  40,    4,  2   },
    { "snake",          2,  15, 1,  0,  0,   0,  3,   0,    3,  1   },
    { "giant centipede",2,  14, 0,  4,  0,   0,  3,   0,    1,  2   },
    { "jaculi",         2,  20, 1,  0,  0,   0,  3,   0,    2,  1   },
    { "troglodyte",     2,  10, 2,  0,  0,   0,  5,  80,    4,  3   },
    { "giant ant",      2,  8,  1,  4,  0,   0,  4,   0,    5,  5   },

    /*  NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
    ----------------------------------------------------------------- */

    { "floating eye",   3,  8,  1,  0,  0,   0,  3,   0,     5,  2  },
    { "leprechaun",     3,  3,  0,  8,  0,   0,  3,1500,    13, 45  },
    { "nymph",          3,  3,  0,  14, 0,   0,  9,   0,    18, 45  },
    { "quasit",         3,  5,  3,  0,  0,   0,  3,   0,    10, 15  },
    { "rust monster",   3,  4,  0,  1,  0,   0,  3,   0,    18, 25  },
    { "zombie",         3,  12, 2,  0,  0,   0,  3,   0,     6,  7  },

    { "assassin bug",   4,  9,  3,  0,  0,   0,  3,   0,    20, 15  },
    { "bugbear",        4,  5,  4,  15, 0,   0,  5,  40,    20, 35  },
    { "hell hound",     4,  5,  2,  2,  0,   0,  6,   0,    16, 35  },
    { "ice lizard",     4,  11, 2,  10, 0,   0,  6,  50,    16, 25  },
    { "centaur",        4,  6,  4,  0,  0,   0, 10,  40,    24, 45  },

    /*  NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
    ----------------------------------------------------------------- */

    { "troll",          5,  4,  5,  0,  0,   0,  9,  80,    50, 300 },
    { "yeti",           5,  6,  4,  0,  0,   0,  5,  50,    35, 100 },
    { "white dragon",   5,  2,  4,  5,  0,   0, 16, 500,    55, 1000},
    { "elf",            5,  8,  1,  0,  0,   0, 15,  50,    22, 35  },
    { "gelatinous cube",5,  9,  1,  0,  0,   0,  3,   0,    22, 45  },

    { "metamorph",      6,  7,  3,  0,  0,   0,  3,  0,     30, 40  },
    { "vortex",         6,  4,  3,  0,  0,   0,  3,  0,     30, 55  },
    { "ziller",         6,  15, 3,  0,  0,   0,  3,  0,     30, 35  },
    { "violet fungi",   6,  12, 3,  0,  0,   0,  3,  0,     38, 100 },
    { "wraith",         6,  3,  1,  6,  0,   0,  3,  0,     30, 325 },
    { "forvalaka",      6,  2,  5,  0,  0,   0,  7,  0,     50, 280 },

    /*  NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
    ----------------------------------------------------------------- */

    { "lama nobe",      7,  7,  3,  0,  0,   0,  6,  0,     35, 80  },
    { "osequip",        7,  4,  3,  16, 0,   0,  4,  0,     35, 100 },
    { "rothe",          7,  15, 5,  0,  0,   0,  3,  100,   50, 250 },
    { "xorn",           7,  0,  6,  0,  0,   0, 13,  0,     60, 300 },
    { "vampire",        7,  3,  4,  6,  0,   0, 17,  0,     50, 1000},
    { "invisible stalker",7,3,  6,  0,  0,   0,  5,  0,     50, 350 },

    { "poltergeist",    8,  1,  4,  0,  0,   0,  3,  0,     50, 450 },
    { "disenchantress", 8,  3,  0,  9,  0,   0,  3,  0,     50, 500 },
    { "shambling mound",8,  2,  5,  0,  0,   0,  6,  0,     45, 400 },
    { "yellow mold",    8,  12, 4,  0,  0,   0,  3,  0,     35, 250 },
    { "umber hulk",     8,  3,  7,  11, 0,   0, 14,  0,     65, 600 },

    /*  NAME            LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
    ----------------------------------------------------------------- */

    { "gnome king",     9,  -1, 10, 0,  0,   0, 18,  2000,  100,3000    },
    { "mimic",          9,   5, 6,  0,  0,   0,  8,  0,     55, 99      },
    { "water lord",     9, -10, 15, 7,  0,   0, 20,  0,     150,15000   },
    { "bronze dragon",  9,   2, 9,  3,  0,   0, 16,  300,   80, 4000    },
    { "green dragon",   9,   3, 8,  10, 0,   0, 15,  200,   70, 2500    },
    { "purple worm",    9,  -1, 11, 0,  0,   0,  3,  100,   120,15000   },
    { "xvart",          9,  -2, 12, 0,  0,   0, 13,  0,     90, 1000    },

    { "spirit naga",    10, -20,12, 12, 0,   0, 23,  0,     95, 20000   },
    { "silver dragon",  10, -1, 12, 3,  0,   0, 20,  700,   100,10000   },
    { "platinum dragon",10, -5, 15, 13, 0,   0, 22,  1000,  130,24000   },
    { "green urchin",   10, -3, 12, 0,  0,   0,  3,  0,     85, 5000    },
    { "red dragon",     10, -2, 13, 3,  0,   0, 19,  800,   110,14000   },

    { "type I demon lord",  12,-30, 18, 0,   0,  0, 20, 0,  140,50000   },
    { "type II demon lord", 13,-30, 18, 0,   0,  0, 21, 0,  160,75000   },
    { "type III demon lord",14,-30, 18, 0,   0,  0, 22, 0,  180,100000  },
    { "type IV demon lord", 15,-35, 20, 0,   0,  0, 23, 0,  200,125000  },
    { "type V demon lord",  16,-40, 22, 0,   0,  0, 24, 0,  220,150000  },
    { "type VI demon lord", 17,-45, 24, 0,   0,  0, 25, 0,  240,175000  },
    { "type VII demon lord",18,-70, 27, 6,   0,  0, 26, 0,  260,200000  },
    { "demon prince",       25,-127,30, 6,   0,  0, 28, 0,  345,300000  }

    /*  NAME                LV  AC  DAM ATT DEF GEN INT GOLD    HP  EXP
    --------------------------------------------------------------------- */
     };
"""

scrollname = [
    "\0enchant armor",
    "\0enchant weapon",
    "\0enlightenment",
    "\0blank paper",
    "\0create monster",
    "\0create artifact",
    "\0aggravate monsters",
    "\0time warp",
    "\0teleportation",
    "\0expanded awareness",
    "\0haste monsters",
    "\0monster healing",
    "\0spirit protection",
    "\0undead protection",
    "\0stealth",
    "\0magic mapping",
    "\0hold monsters",
    "\0gem perfection",
    "\0spell extension",
    "\0identify",
    "\0remove curse",
    "\0annihilation",
    "\0pulverization",
    "\0life protection",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0zzzzzzzzzzzzzz"    # /* sentinel, for the sorted known objects inventory */
]  # type: List[str]
""" /*  name array for scrolls      */
    char scrollname[MAXSCROLL+1][MAXSCROLLNAME] = {
    "\0enchant armor",
    "\0enchant weapon",
    "\0enlightenment",
    "\0blank paper",
    "\0create monster",
    "\0create artifact",
    "\0aggravate monsters",
    "\0time warp",
    "\0teleportation",
    "\0expanded awareness",
    "\0haste monsters",
    "\0monster healing",
    "\0spirit protection",
    "\0undead protection",
    "\0stealth",
    "\0magic mapping",
    "\0hold monsters",
    "\0gem perfection",
    "\0spell extension",
    "\0identify",
    "\0remove curse",
    "\0annihilation",
    "\0pulverization",
    "\0life protection",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0zzzzzzzzzzzzzz"    /* sentinel, for the sorted known objects inventory */
     };
"""

potionname = [
    "\0sleep",
    "\0healing",
    "\0raise level",
    "\0increase ability",
    "\0wisdom",
    "\0strength",
    "\0raise charisma",
    "\0dizziness",
    "\0learning",
    "\0object detection",
    "\0monster detection",
    "\0forgetfulness",
    "\0water",
    "\0blindness",
    "\0confusion",
    "\0heroism",
    "\0sturdiness",
    "\0giant strength",
    "\0fire resistance",
    "\0treasure finding",
    "\0instant healing",
    " cure dianthroritis",
    "\0poison",
    "\0see invisible",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0zzzzzzzzzzzzzz"    # /* sentinel, for the sorted known objects inventory */
]  # type: List[str]
""" /*  name array for magic potions    */
    char potionname[MAXPOTION+1][MAXPOTIONNAME] = {
    "\0sleep",
    "\0healing",
    "\0raise level",
    "\0increase ability",
    "\0wisdom",
    "\0strength",
    "\0raise charisma",
    "\0dizziness",
    "\0learning",
    "\0object detection",
    "\0monster detection",
    "\0forgetfulness",
    "\0water",
    "\0blindness",
    "\0confusion",
    "\0heroism",
    "\0sturdiness",
    "\0giant strength",
    "\0fire resistance",
    "\0treasure finding",
    "\0instant healing",
    " cure dianthroritis",
    "\0poison",
    "\0see invisible",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0 ",
    "\0zzzzzzzzzzzzzz"    /* sentinel, for the sorted known objects inventory */
    };
"""

# /*
#     spell data
#  */
spelknow = [0] * SPNUM  # type: List[int]
""" signed char spelknow[SPNUM];
"""
splev = [
    1, 4, 9, 14, 18, 22, 26, 29, 32, 35, 37, 37, 37, 37, 37 
]  # type: List[int]
""" signed char splev[] = { 1, 4, 9, 14, 18, 22, 26, 29, 32, 35, 37, 37, 37, 37, 37 };
"""

spelcode = [
    "pro",  "mle",  "dex",  "sle",  "chm",  "ssp",
    "web",  "str",  "enl",  "hel",  "cbl",  "cre",  "pha",  "inv",
    "bal",  "cld",  "ply",  "can",  "has",  "ckl",  "vpr",
    "dry",  "lit",  "drl",  "glo",  "flo",  "fgr",
    "sca",  "hld",  "stp",  "tel",  "mfi", # /* 31 */
    "sph",  "gen",  "sum",  "wtw",  "alt",  "per", "zzz"
]  # type: List[str]
""" char *spelcode[SPNUM+1]={
        "pro",  "mle",  "dex",  "sle",  "chm",  "ssp",
        "web",  "str",  "enl",  "hel",  "cbl",  "cre",  "pha",  "inv",
        "bal",  "cld",  "ply",  "can",  "has",  "ckl",  "vpr",
        "dry",  "lit",  "drl",  "glo",  "flo",  "fgr",
        "sca",  "hld",  "stp",  "tel",  "mfi", /* 31 */
        "sph",  "gen",  "sum",  "wtw",  "alt",  "per", "zzz"
     };
"""

spelname = [
    "protection",               "magic missile",        "dexterity",
    "sleep",                    "charm monster",        "sonic spear",

    "web",                      "strength",             "enlightenment",
    "healing",                  "cure blindness",       "create monster",
    "phantasmal forces",        "invisibility",

    "fireball",                 "cold",                 "polymorph",
    "cancellation",             "haste self",           "cloud kill",
    "vaporize rock",

    "dehydration",              "lightning",            "drain life",
    "invulnerability",          "flood",                "finger of death",

    "scare monster",            "hold monster",         "time stop",
    "teleport away",            "magic fire",

    "sphere of annihilation",   "genocide",             "summon demon",
    "walk through walls",       "alter reality",        "permanence",
    ""
]  # type: List[str]
""" char *spelname[]={
        "protection",               "magic missile",        "dexterity",
        "sleep",                    "charm monster",        "sonic spear",

        "web",                      "strength",             "enlightenment",
        "healing",                  "cure blindness",       "create monster",
        "phantasmal forces",        "invisibility",

        "fireball",                 "cold",                 "polymorph",
        "cancellation",             "haste self",           "cloud kill",
        "vaporize rock",

        "dehydration",              "lightning",            "drain life",
        "invulnerability",          "flood",                "finger of death",

        "scare monster",            "hold monster",         "time stop",
        "teleport away",            "magic fire",

        "sphere of annihilation",   "genocide",             "summon demon",
        "walk through walls",       "alter reality",        "permanence",
        ""
     };
"""

speldescript = [
# /* 1 */
    "generates a +2 protection field",
    "creates and hurls a magic missile equivalent to a + 1 magic arrow",
    "adds +2 to the casters dexterity",
    "causes some monsters to go to sleep",
    "some monsters may be awed at your magnificence",
    "causes your hands to emit a screeching sound toward what they point",
# /* 7 */
    "causes strands of sticky thread to entangle an enemy",
    "adds +2 to the casters strength for a short term",
    "the caster becomes aware of things around him",
    "restores some hp to the caster",
    "restores sight to one so unfortunate as to be blinded",
    "creates a monster near the caster appropriate for the location",
    "creates illusions, and if believed, monsters die",
    "the caster becomes invisible",
# /* 15 */
    "makes a ball of fire that burns on what it hits",
    "sends forth a cone of cold which freezes what it touches",
    "you can find out what this does for yourself",
    "negates the ability of a monster to use his special abilities",
    "speeds up the casters movements",
    "creates a fog of poisonous gas which kills all that is within it",
    "this changes rock to air",
# /* 22 */
    "dries up water in the immediate vicinity",
    "you finger will emit a lightning bolt when this spell is cast",
    "subtracts hit points from both you and a monster",
    "this globe helps to protect the player from physical attack",
    "this creates an avalanche of H2O to flood the immediate chamber",
    "this is a holy spell and calls upon your god to back you up",
# /* 28 */
    "terrifies the monster so that hopefully he wont hit the magic user",
    "the monster is frozen in his tracks if this is successful",
    "all movement in the caverns ceases for a limited duration",
    "moves a particular monster around in the dungeon (hopefully away from you)",
    "this causes a curtain of fire to appear all around you",
# /* 33 */
    "anything caught in this sphere is instantly killed.  Warning -- dangerous",
    "eliminates a species of monster from the game -- use sparingly",
    "summons a demon who hopefully helps you out",
    "allows the player to walk through walls for a short period of time",
    "god only knows what this will do",
    "makes a character spell permanent, i. e. protection, strength, etc.",
    ""
]  # type: List[str]
""" char *speldescript[]={
    /* 1 */
        "generates a +2 protection field",
        "creates and hurls a magic missile equivalent to a + 1 magic arrow",
        "adds +2 to the casters dexterity",
        "causes some monsters to go to sleep",
        "some monsters may be awed at your magnificence",
        "causes your hands to emit a screeching sound toward what they point",
    /* 7 */
        "causes strands of sticky thread to entangle an enemy",
        "adds +2 to the casters strength for a short term",
        "the caster becomes aware of things around him",
        "restores some hp to the caster",
        "restores sight to one so unfortunate as to be blinded",
        "creates a monster near the caster appropriate for the location",
        "creates illusions, and if believed, monsters die",
        "the caster becomes invisible",
    /* 15 */
        "makes a ball of fire that burns on what it hits",
        "sends forth a cone of cold which freezes what it touches",
        "you can find out what this does for yourself",
        "negates the ability of a monster to use his special abilities",
        "speeds up the casters movements",
        "creates a fog of poisonous gas which kills all that is within it",
        "this changes rock to air",
    /* 22 */
        "dries up water in the immediate vicinity",
        "you finger will emit a lightning bolt when this spell is cast",
        "subtracts hit points from both you and a monster",
        "this globe helps to protect the player from physical attack",
        "this creates an avalanche of H2O to flood the immediate chamber",
        "this is a holy spell and calls upon your god to back you up",
    /* 28 */
        "terrifies the monster so that hopefully he wont hit the magic user",
        "the monster is frozen in his tracks if this is successful",
        "all movement in the caverns ceases for a limited duration",
        "moves a particular monster around in the dungeon (hopefully away from you)",
        "this causes a curtain of fire to appear all around you",
    /* 33 */
        "anything caught in this sphere is instantly killed.  Warning -- dangerous",
        "eliminates a species of monster from the game -- use sparingly",
        "summons a demon who hopefully helps you out",
        "allows the player to walk through walls for a short period of time",
        "god only knows what this will do",
        "makes a character spell permanent, i. e. protection, strength, etc.",
        ""
     };
"""

# Weird responses to spells. This is a monster->spellnum->table-index lookup
# into a messages table below. It should be replaced by a nested? dictionary.
spelweird = [
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*            bat */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          gnome */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*      hobgoblin */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         jackal */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         kobold */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*            orc */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          snake */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*giant centipede */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         jaculi */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     troglodyte */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*      giant ant */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   floating eye */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     leprechaun */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          nymph */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         quasit */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   rust monster */
[  0,0,0,8,0,4,   0,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         zombie */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   assassin bug */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*        bugbear */
[  0,6,0,0,0,0,   12,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     hell hound */
[  0,0,0,0,0,0,   11,0,0,0,0,0,0,0,  0,15,0,0,0,0,0,  0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     ice lizard */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*        centaur */
[  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          troll */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,15,0,0,0,0,0,  0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*           yeti */
[  0,0,0,0,0,0,   0,0,0,0,0,0,14,0,  0,15,0,0,0,0,0,  4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   white dragon */
[  0,0,0,0,0,0,   0,0,0,0,0,0,14,5,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*            elf */
[  0,0,0,0,0,0,   2,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   0,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*gelatinous cube */
[  0,13,0,0,0,0,  2,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*      metamorph */
[  0,13,0,0,0,10, 1,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         vortex */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         ziller */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   violet fungi */
[  0,0,0,8,0,4,   0,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*         wraith */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*      forvalaka */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*      lama nobe */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*        osequip */
[  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          rothe */
[  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*           xorn */
[  0,0,0,8,0,4,   0,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   0,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*        vampire */
[  0,0,0,0,0,0,   1,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*invisible staker*/
[  0,13,0,8,0,4,  1,0,0,0,0,0,0,0,   0,4,0,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*    poltergeist */
[  0,0,0,8,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /* disenchantress */
[  0,0,0,0,0,10,  0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*shambling mound */
[  0,0,0,8,0,0,   1,0,0,0,0,0,4,0,   0,0,0,0,0,4,0,   0,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*    yellow mold */
[  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     umber hulk */
[  0,7,0,0,3,0,   0,0,0,0,0,0,0,5,   0,0,9,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     gnome king */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          mimic */
[  0,13,0,8,3,4,  1,0,0,0,0,0,0,0,   0,0,9,0,0,4,0,   0,0,0,0,16,4,  0,0,0,0,0,   0,0,0,0,0,0 ], # /*     water lord */
[  0,7,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*  bronze dragon */
[  0,7,0,0,0,0,   11,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   green dragon */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*    purple worm */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*          xvart */
[  0,13,0,8,3,4,  1,0,0,0,0,0,0,5,   0,4,9,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*    spirit naga */
[  0,6,0,9,0,0,   12,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*  silver dragon */
[  0,7,0,9,0,0,   11,0,0,0,0,0,14,0, 0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*platinum dragon */
[  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*   green urchin */
[  0,6,0,0,0,0,   12,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 ], # /*     red dragon */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 ], # /*     demon lord */
[  0,7,0,4,3,9,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   4,0,0,0,4,   9,0,0,0,0,0 ], # /*   demon prince */
]  # type: List[List[int]]
""" signed char spelweird[MAXMONST+8][SPNUM] = {
    /*                      p m d s c s    w s e h c c p i    b c p c h c v    d l d g f f    s h s t m    s g s w a p */
    /*                      r l e l h s    e t n e b r h n    a l l a a k p    r i r l l g    c l t e f    p e u t l e */
    /*                      o e x e m p    b r l l l e a v    l d y n s l r    y t l o o r    a d p l i    h n m w t r */


    /*            bat */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*          gnome */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*      hobgoblin */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         jackal */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         kobold */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*            orc */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*          snake */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*giant centipede */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         jaculi */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     troglodyte */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*      giant ant */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*   floating eye */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     leprechaun */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*          nymph */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         quasit */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*   rust monster */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         zombie */ {  0,0,0,8,0,4,   0,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*   assassin bug */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*        bugbear */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     hell hound */ {  0,6,0,0,0,0,   12,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*     ice lizard */ {  0,0,0,0,0,0,   11,0,0,0,0,0,0,0,  0,15,0,0,0,0,0,  0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*        centaur */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*          troll */ {  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*           yeti */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,15,0,0,0,0,0,  0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*   white dragon */ {  0,0,0,0,0,0,   0,0,0,0,0,0,14,0,  0,15,0,0,0,0,0,  4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*            elf */ {  0,0,0,0,0,0,   0,0,0,0,0,0,14,5,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*gelatinous cube */ {  0,0,0,0,0,0,   2,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   0,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*      metamorph */ {  0,13,0,0,0,0,  2,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         vortex */ {  0,13,0,0,0,10, 1,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         ziller */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*   violet fungi */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*         wraith */ {  0,0,0,8,0,4,   0,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   4,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*      forvalaka */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*      lama nobe */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*        osequip */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*          rothe */ {  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*           xorn */ {  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   4,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*        vampire */ {  0,0,0,8,0,4,   0,0,0,0,0,0,0,0,   0,0,0,0,0,4,0,   0,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*invisible staker*/ {  0,0,0,0,0,0,   1,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*    poltergeist */ {  0,13,0,8,0,4,  1,0,0,0,0,0,0,0,   0,4,0,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   0,0,0,0,0,0 },

    /* disenchantress */ {  0,0,0,8,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*shambling mound */ {  0,0,0,0,0,10,  0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*    yellow mold */ {  0,0,0,8,0,0,   1,0,0,0,0,0,4,0,   0,0,0,0,0,4,0,   0,0,0,0,0,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     umber hulk */ {  0,7,0,0,0,0,   0,0,0,0,0,0,0,5,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     gnome king */ {  0,7,0,0,3,0,   0,0,0,0,0,0,0,5,   0,0,9,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*          mimic */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     water lord */ {  0,13,0,8,3,4,  1,0,0,0,0,0,0,0,   0,0,9,0,0,4,0,   0,0,0,0,16,4,  0,0,0,0,0,   0,0,0,0,0,0 },
    /*  bronze dragon */ {  0,7,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*   green dragon */ {  0,7,0,0,0,0,   11,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*    purple worm */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*          xvart */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*    spirit naga */ {  0,13,0,8,3,4,  1,0,0,0,0,0,0,5,   0,4,9,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*  silver dragon */ {  0,6,0,9,0,0,   12,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*platinum dragon */ {  0,7,0,9,0,0,   11,0,0,0,0,0,14,0, 0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*   green urchin */ {  0,0,0,0,0,0,   0,0,0,0,0,0,0,0,   0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },
    /*     red dragon */ {  0,6,0,0,0,0,   12,0,0,0,0,0,0,0,  0,0,0,0,0,0,0,   0,0,0,0,0,0,   0,0,0,0,0,   0,0,0,0,0,0 },

    /*                      p m d s c s    w s e h c c p i    b c p c h c v    d l d g f f    s h s t m    s g s w a p */
    /*                      r l e l h s    e t n e b r h n    a l l a a k p    r i r l l g    c l t e f    p e u t l e */
    /*                      o e x e m p    b r l l l e a v    l d y n s l r    y t l o o r    a d p l i    h n m w t r */

    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*     demon lord */ {  0,7,0,4,3,0,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   0,0,0,0,0,   9,0,0,0,0,0 },
    /*   demon prince */ {  0,7,0,4,3,9,   1,0,0,0,0,0,14,5,  0,0,4,0,0,4,0,   4,0,0,0,4,4,   4,0,0,0,4,   9,0,0,0,0,0 }

     };
"""

# This is the lookup table referenced above in spelweird.
spelmes = [
    "",
    "the web had no effect on the %s",         # /*  1 */
    "the %s changed shape to avoid the web",   # /*  2 */
    "the %s isn't afraid of you",              # /*  3 */
    "the %s isn't affected",                   # /*  4 */
    "the %s can see you with his infravision", # /*  5 */
    "the %s vaporizes your missile",           # /*  6 */
    "your missile bounces off the %s",         # /*  7 */
    "the %s doesn't sleep",                    # /*  8 */
    "the %s resists",                          # /*  9 */
    "the %s can't hear the noise",             # /* 10 */
    "the %s's tail cuts it free of the web",   # /* 11 */
    "the %s burns through the web",            # /* 12 */
    "your missiles pass right through the %s", # /* 13 */
    "the %s sees through your illusions",      # /* 14 */
    "the %s loves the cold!",                  # /* 15 */
    "the %s loves the water!"                  # /* 16 */
]  # type: List[str]
""" char *spelmes[] = { "",
    /*  1 */    "the web had no effect on the %s",
    /*  2 */    "the %s changed shape to avoid the web",
    /*  3 */    "the %s isn't afraid of you",
    /*  4 */    "the %s isn't affected",
    /*  5 */    "the %s can see you with his infravision",
    /*  6 */    "the %s vaporizes your missile",
    /*  7 */    "your missile bounces off the %s",
    /*  8 */    "the %s doesn't sleep",
    /*  9 */    "the %s resists",
    /* 10 */    "the %s can't hear the noise",
    /* 11 */    "the %s's tail cuts it free of the web",
    /* 12 */    "the %s burns through the web",
    /* 13 */    "your missiles pass right through the %s",
    /* 14 */    "the %s sees through your illusions",
    /* 15 */    "the %s loves the cold!",
    /* 16 */    "the %s loves the water!"
     };
"""



















scprob = [ 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3,
    3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 9, 9,
    9, 9, 10, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13, 14, 14,
    15, 15, 16, 16, 16, 17, 17, 18, 18, 19, 19, 19, 20, 20, 20, 20, 21, 22,
    22, 22, 23 ]  # type: List[int]
""" /*
     *  function to create scroll numbers with appropriate probability of 
     *  occurrence
     *
     *  0 - armor           1 - weapon      2 - enlightenment   3 - paper
     *  4 - create monster  5 - create item 6 - aggravate       7 - time warp
     *  8 - teleportation   9 - expanded awareness              10 - haste monst
     *  11 - heal monster   12 - spirit protection      13 - undead protection
     *  14 - stealth        15 - magic mapping          16 - hold monster
     *  17 - gem perfection 18 - spell extension        19 - identify
     *  20 - remove curse   21 - annihilation           22 - pulverization
     *  23 - life protection
     */
"""

potprob = [ 0, 0, 1, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 9, 9, 9,
           10, 10, 10, 11, 11, 12, 12, 13, 14, 15, 16, 17, 18, 19, 19, 19,
           20, 20, 22, 22, 23, 23 ]  # type: List[int]
""" /*
     *  function to return a potion number created with appropriate probability
     *  of occurrence
     *
     *  0 - sleep               1 - healing                 2 - raise level
     *  3 - increase ability    4 - gain wisdom             5 - gain strength
     *  6 - increase charisma   7 - dizziness               8 - learning
     *  9 - object detection    10 - monster detection      11 - forgetfulness
     *  12 - water              13 - blindness              14 - confusion
     *  15 - heroism            16 - sturdiness             17 - giant strength
     *  18 - fire resistance    19 - treasure finding       20 - instant healing
     *  21 - cure dianthroritis 22 - poison                 23 - see invisible
     */
"""
nlpts = [ 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7 ]  # type: List[int]
nch = [ 0, 0, 0, 1, 1, 1, 2, 2, 3, 4 ]  # type: List[int]
nplt = [ 0, 0, 0, 0, 1, 1, 2, 2, 3, 4 ]  # type: List[int]
ndgg = [ 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5 ]  # type: List[int]
nsw = [ 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 3 ]  # type: List[int]
