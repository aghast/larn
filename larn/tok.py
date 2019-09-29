""" 
    /* tok.c */
    /*
       yylex()
       flushall()
       sethard()
    */
"""

from .larncons import *
from .larndata import *
from .larnfunc import *

CHKPTINT = 400
""" # define CHKPTINT   400 """

# static
lastok: char = 0
#yrepcount: int = 0
#move_no_pickup: signed_char = False


def yylex() -> str:
    """ lexical analyzer for larn
    """
    global yrepcount, move_no_pickup

    firsttime: char = True

    if hit2flag:
        hit2flag = 0
        yrepcount = 0
        return ' '

    if yrepcount > 0:
        yrepcount -= 1
        return lastok
    else:
        yrepcount = 0

    if yrepcount == 0:
        bottomdo()
        showplayer()
        move_no_pickup = False

    lflush()

    while True:
        c[BYTESIN] += 1
        cc = ttgetch()

        if cc.isdigit():
            # get repeat count, showing to player
            yrepcount = yrepcount * 10 + int(cc)

            if yrepcount >= 10:
                cursors()
                if firsttime:
                    lprcat("\n")

                lprintf("count: %d", yrepcount)
                firsttime = False
                lflush()
        else: 
            # check for multi-character commands and handle.
            if cc == 'm':
                move_no_pickup = True
                cc = ttgetch()
            
            if yrepcount > 0:
                yrepcount -= 1

            lastok = cc
            return lastok


def sethard(hard: int) -> None:
    """ void sethard(int hard)
        /*
            function to set the desired hardness
            enter with hard= -1 for default hardness, else any desired hardness
         */

         WHY IS THIS HERE? In this file? WTF?
    """

    j = c[HARDGAME]
    hashewon()

    # don't set c[HARDGAME] if restoring game

    if restorflag == 0:
        if hard >= 0:
            c[HARDGAME] = hard
    else:
        # set c[HARDGAME] to proper value if restoring game
        c[HARDGAME] = j

    k = c[HARDGAME]
    if k == 0:
        return

    for j in range(MAXMONST + 9):   # + 9 ???
        mp = monster[j]
        i = ((6 + k) * mp.hitpoints + 1) // 6
        mp.hitpoints = min(i, 32767)

        i = ((6 + k) * mp.damage + 1) // 5
        mp.damage = min(i, 127)

        i = (10 * mp.gold) // (10 + k)
        mp.gold = min(i, 32767)

        i = mp.armorclass - k
        mp.armorclass = max(i, -127)

        i = (7 * mp.experience) // (7 + 1) + 1
        mp.experience = max(i, 1)
