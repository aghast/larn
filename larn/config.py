""" config.py
/*
 *  config.c    --  This defines the installation dependent variables.
 *                  Some strings are modified later.  ANSI C would
 *                  allow compile time string concatenation, we must
 *                  do runtime concatenation, in main.
 */
"""
from aghast.util import export

EXTRA: bool = False   # #define EXTRA 0
export('EXTRA')

WIZID: int = 1000        # #define WIZID 0
export('WIZID')

#
# All these strings will be appended to in main() to be complete filenames
#

# Make LARNHOME readable from the larnopt file into a lardir variable.

savefilename: str = ""  # char savefilename[PATHLEN];
export('savefilename')
scorefile: str = ""	    # char scorefile[PATHLEN];
export('scorefile')
logfile: str = ""	    # char logfile[PATHLEN];
export('logfile')
helpfile: str = ""	    # char helpfile[PATHLEN];
export('helpfile')
larnlevels: str = ""	# char larnlevels[PATHLEN];
export('larnlevels')
fortfile: str = ""	    # char fortfile[PATHLEN];
export('fortfile')
playerids: str = ""	    # char playerids[PATHLEN];
export('playerids')

if EXTRA:
    diagfile: str = ""  # char diagfile[PATHLEN]; /* the diagnostic filename  */
    export('diagfile')

password: str = "pvnert(x)" # char *password ="pvnert(x)";/* the wizards password <=32*/
export('password')

