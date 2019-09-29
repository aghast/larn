""" larn/larncons.py

    Constants.
"""

from .config import *

PATCHLEVEL: int = 0

# /* defines below are for use in the termcap mode only */
ST_START: str = chr(1)
ST_END: str =   chr(2)
BOLD: int =     3
END_BOLD: int = 4
CLEAR: int =    5
CL_LINE: int =  6
T_INIT: int =   7
T_END: int =    8
CL_DOWN: int = 14
CURSOR: int =  15


KNOWNOT: int =    0x00
HAVESEEN: int =   0x1
KNOWHERE: int =   0x2
KNOWALL: int =    (HAVESEEN | KNOWHERE)

PATHLEN: int =    80

LARNHOME: str =  ""

# I'll just use the Python builtins, thanks.
#define TRUE 1
#define FALSE 0

SCORENAME: str =  "larn.scr"
LOGFNAME: str =   "larn.log"
HELPNAME: str =   "larn.hlp"
LEVELSNAME: str = "larn.maz"
FORTSNAME: str =  "larn.ftn"
PLAYERIDS: str =  "larn.pid"
DIAGFILE: str =   "diagfile"
SAVEFILE: str =   "larn.sav"


MAXLEVEL: int =  11  # /*  max # levels in the dungeon         */
MAXVLEVEL: int =  3  # /*  max # of levels in the temple of the luran  */
MAXX: int =  67
MAXY: int =  17

SCORESIZE: int = 10  # /* this is the number of people on a scoreboard max */
MAXPLEVEL: int = 100  # /* maximum player level allowed        */
SPNUM: int =  38  # /* maximum number of spells in existance   */
TIMELIMIT: int = 30000  # /* maximum number of moves before the game is called */
TAXRATE: float = 1.0 / 20  # /* tax rate for the LRS */

BUFBIG: int = 4096  # /* size of the output buffer */
MAXIBUF: int = 4096  # /* size of the input buffer */
LOGNAMESIZE: int =  20  # /* max size of the player's name */

SAVEFILENAMESIZE: int = 128  # /* max size of the savefile path */

STRING_BUFFER_SIZE: int = 256

# 
# monster related constants
# 

MAXMONST: int =  56  #   /* maximum # monsters in the dungeon */

# /*  defines for the monsters as objects  */
BAT: int =  1
GNOME: int =  2
HOBGOBLIN: int =  3
JACKAL: int =  4
KOBOLD: int =  5
ORC: int =  6
SNAKE: int =  7
CENTIPEDE: int =  8
JACULI: int =  9
TROGLODYTE: int =  10
ANT: int =  11
EYE: int =  12 
LEPRECHAUN: int =  13
NYMPH: int =  14
QUASIT: int =  15 
RUSTMONSTER: int =  16 
ZOMBIE: int =  17 
ASSASSINBUG: int =  18 
BUGBEAR: int =  19 
HELLHOUND: int =  20 
ICELIZARD: int =  21 
CENTAUR: int =  22 
TROLL: int =  23 
YETI: int =  24 
WHITEDRAGON: int =  25
ELF: int =  26
CUBE: int =  27 
METAMORPH: int =  28 
VORTEX: int =  29 
ZILLER: int =  30 
VIOLETFUNGI: int =  31 
WRAITH: int =  32 
FORVALAKA: int =  33 
LAMANOBE: int =  34 
OSEQUIP: int =  35 
ROTHE: int =  36
XORN: int =  37
VAMPIRE: int =  38
INVISIBLESTALKER: int =  39
POLTERGEIST: int =  40
DISENCHANTRESS: int =  41
SHAMBLINGMOUND: int =  42
YELLOWMOLD: int =  43
UMBERHULK: int =  44
GNOMEKING: int =  45
MIMIC: int =  46
WATERLORD: int =  47
BRONZEDRAGON: int =  48
GREENDRAGON: int =  49
PURPLEWORM: int =  50
XVART: int =  51
SPIRITNAGA: int =  52
SILVERDRAGON: int =  53
PLATINUMDRAGON: int =  54
GREENURCHIN: int =  55
REDDRAGON: int =  56
DEMONLORD: int =  57
DEMONPRINCE: int =  64




#   
#  defines for the character attribute array   c[] 
# 

STRENGTH: int =  0  # /* characters physical strength not due to objects */
INTELLIGENCE: int =  1
WISDOM: int =  2
CONSTITUTION: int =  3
DEXTERITY: int =  4
CHARISMA: int =  5
HPMAX: int =  6
HP: int =  7
GOLD: int =  8
EXPERIENCE: int =  9
LEVEL: int =  10
REGEN: int =  11
WCLASS: int =  12
AC: int =  13
BANKACCOUNT: int =  14
SPELLMAX: int =  15
SPELLS: int =  16
ENERGY: int =  17
ECOUNTER: int =  18
MOREDEFENSES: int =  19
WEAR: int =  20
PROTECTIONTIME: int =  21
WIELD: int =  22
AMULET: int =  23
REGENCOUNTER: int =  24
MOREDAM: int =  25
DEXCOUNT: int =  26
STRCOUNT: int =  27
BLINDCOUNT: int =  28
CAVELEVEL: int =  29
CONFUSE: int =  30
ALTPRO: int =  31
HERO: int =  32
CHARMCOUNT: int =  33
INVISIBILITY: int =  34
CANCELLATION: int =  35
HASTESELF: int =  36
EYEOFLARN: int =  37
AGGRAVATE: int =  38
GLOBE: int =  39
TELEFLAG: int =  40
SLAYING: int =  41
NEGATESPIRIT: int =  42
SCAREMONST: int =  43
AWARENESS: int =  44
HOLDMONST: int =  45
TIMESTOP: int =  46
HASTEMONST: int =  47
CUBEofUNDEAD: int =  48
GIANTSTR: int =  49
FIRERESISTANCE: int =  50
BESSMANN: int =  51
NOTHEFT: int =  52
HARDGAME: int =  53
CPUTIME: int =  54
BYTESIN: int =  55
BYTESOUT: int =  56
MOVESMADE: int =  57
MONSTKILLED: int =  58
SPELLSCAST: int =  59
LANCEDEATH: int =  60
SPIRITPRO: int =  61
UNDEADPRO: int =  62
SHIELD: int =  63
STEALTH: int =  64
ITCHING: int =  65
LAUGHING: int =  66
DRAINSTRENGTH: int =  67
CLUMSINESS: int =  68
INFEEBLEMENT: int =  69
HALFDAM: int =  70
SEEINVISIBLE: int =  71
FILLROOM: int =  72
RANDOMWALK: int =  73
SPHCAST: int =  74  # /* nz if an active sphere of annihilation */
WTW: int =  75      # /* walk through walls */
STREXTRA: int =  76 # /* character strength due to objects or enchantments */
TMP: int =  77      # /* misc scratch space */
LIFEPROT: int =  78 # /* life protection counter */





# 
# object related constants
# 

MAXSCROLL: int =  28  #  /* maximum number of scrolls that are possible */
MAXSCROLLNAME: int = 32

MAXPOTION: int =  35  #  /* maximum number of potions that are possible */
MAXPOTIONNAME: int = 32

MAXOBJ: int =  93     #  /* the maximum number of objects   n < MAXOBJ */

# /*  defines for the objects in the game     */
MAXOBJECT: int =   92

OALTAR: int =  1
OTHRONE: int =  2
OORB: int =  3
OPIT: int =  4
OSTAIRSUP: int =  5
OELEVATORUP: int =  6
OFOUNTAIN: int =  7
OSTATUE: int =  8
OTELEPORTER: int =  9
OSCHOOL: int =  10
OMIRROR: int =  11
ODNDSTORE: int =  12
OSTAIRSDOWN: int =  13
OELEVATORDOWN: int =  14
OBANK2: int =  15
OBANK: int =  16
ODEADFOUNTAIN: int =  17
OMAXGOLD: int =  70
OGOLDPILE: int =  18
OOPENDOOR: int =  19
OCLOSEDDOOR: int =  20
OWALL: int =  21
OTRAPARROW: int =  66
OTRAPARROWIV: int =  67

OLARNEYE: int =  22

OPLATE: int =  23
OCHAIN: int =  24
OLEATHER: int =  25
ORING: int =  60
OSTUDLEATHER: int =  61
OSPLINT: int =  62
OPLATEARMOR: int =  63
OSSPLATE: int =  64
OSHIELD: int =  68
OELVENCHAIN: int =  92

OSWORDofSLASHING: int =  26
OHAMMER: int =  27
OSWORD: int =  28
O2SWORD: int =  29
OSPEAR: int =  30
ODAGGER: int =  31
OBATTLEAXE: int =  57
OLONGSWORD: int =  58
OFLAIL: int =  59
OLANCE: int =  65
OVORPAL: int =  90
OSLAYER: int =  91

ORINGOFEXTRA: int =  32
OREGENRING: int =  33
OPROTRING: int =  34
OENERGYRING: int =  35
ODEXRING: int =  36
OSTRRING: int =  37
OCLEVERRING: int =  38
ODAMRING: int =  39

OBELT: int =  40

OSCROLL: int =  41
OPOTION: int =  42
OBOOK: int =  43
OCHEST: int =  44             
OAMULET: int =  45

OORBOFDRAGON: int =  46
OSPIRITSCARAB: int =  47
OCUBEofUNDEAD: int =  48
ONOTHEFT: int =  49

ODIAMOND: int =  50
ORUBY: int =  51
OEMERALD: int =  52
OSAPPHIRE: int =  53

OENTRANCE: int =  54
OVOLDOWN: int =  55
OVOLUP: int =  56
OHOME: int =  69

OKGOLD: int =  71
ODGOLD: int =  72
OIVDARTRAP: int =  73
ODARTRAP: int =  74
OTRAPDOOR: int =  75
OIVTRAPDOOR: int =  76
OTRADEPOST: int =  77
OIVTELETRAP: int =  78
ODEADTHRONE: int =  79
OANNIHILATION: int =  80 #       /* sphere of annihilation */
OTHRONE2: int =  81
OLRS: int =  82         #    /* Larn Revenue Service */
OCOOKIE: int =  83
OURN: int =  84
OBRASSLAMP: int =  85
OHANDofFEAR: int =  86  #    /* hand of fear */
OSPHTAILSMAN: int =  87 #    /* tailsman of the sphere */
OWWAND: int =  88       #    /* wand of wonder */
OPSTAFF: int =  89      #    /* staff of power */
# /* used up to 92 */

