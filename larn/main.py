""" larn/main.py

    /* main.c */

    #include <stdlib.h>
    #include <stdio.h>
    #include <string.h>
    #include <errno.h>
    #include <setjmp.h>

    #include "larncons.h"
    #include "larndata.h"
    #include "larnfunc.h"

"""
import os
import sys
from typing import *

from .data import *
from .io import *

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

dropflag = 0  # type: int
""" int dropflag=0; /* if 1 then don't lookforobject() next round */ 
"""
rmst = 80  # type: int
""" int rmst=80;    /*  random monster creation counter     */
"""
userid = 0  # type: int
""" int userid;     /* the players login user id number */
"""
nomove = 0  # type: int
""" signed char nomove=0; /* if (nomove) then don't count next iteration as a
                              move */
"""
viewflag = 0  # type: int
""" static char viewflag=0;    /* if viewflag then we have done a 99 stay here
                                  and don't showcell in the main loop */
"""
restorflag = 0  # type: int
""" signed char restorflag=0;         /* 1 means restore has been done    */
"""

cmdhelp = """\
Cmd line format: larn [-slicnhp] [-##] [++]
  -s   show the scoreboard
  -l   show the logfile (wizard id only)
  -i   show scoreboard with inventories of dead characters
  -c   create new scoreboard (wizard id only)
  -##  specify level of difficulty (example: -5)
  -h   print this help text
"""
""" static char cmdhelp[] = "\
            Cmd line format: larn [-slicnhp] [-##] [++]\n\
            -s   show the scoreboard\n\
            -l   show the logfile (wizard id only)\n\
            -i   show scoreboard with inventories of dead characters\n\
            -c   create new scoreboard (wizard id only)\n\
            -##  specify level of difficulty (example: -5)\n\
            -h   print this help text\n\
            ";
"""

save_mode = 0  # type: int
""" signed int save_mode = 0;      /* 1 if doing a save game */
"""

#
#   ************
#   MAIN PROGRAM
#   ************
# 
def main(argv) -> int:
    hard = -1  # type: int

    # 
    #  first task is to identify the player
    #
    init_term()  # /* setup the terminal (find out what type) for termcap */
    ptr = "PLAYER"  # type: str

    #
    # second task is to prepare the pathnames the player will need
    #
    global logname
    logname = ptr[:]   # this will be replaced by player's name

    # Set up the input and output buffers.
    try:
        global lpbuf
        lpbuf = bytearray((5 * BUFBIG) >> 2)  # output buffer
        global inbuffer
        inbuffer = bytearray((5 * MAXIBUF) >> 2)  # output buffer [[??? --agh]]
    except MemoryError as err:
        died(-285)    # malloc() failure

    assert lpbuf is not None
    assert inbuffer is not None
    
    global savefilename
    savefilename = SAVEFILE[:]

    global scorefile
    scorefile = SCORENAME[:]        # /* the larn scoreboard filename */

    global logfile
    logfile = LOGFNAME[:]           # /* larn activity logging filename */

    global helpfile
    helpfile = HELPNAME[:]          # /* the larn on-line help file */

    global larnlevels
    larnlevels = LEVELSNAME[:]      # /* the pre-made cave level data file */

    global fortfile
    fortfile = FORTSNAME[:]         # /* the fortune data file name */

    global playerids
    playerids = PLAYERIDS[:]        # /* the playerid data file name */

    if EXTRA:
        global diagfile
        diagfile = DIAGFILE[:]      # #ifdef EXTRA ... #endif

    #
    #   now make scoreboard if it is not there (don't clear) 
    #
    if not os.access(scorefile, os.F_OK):   # Not there?
        makeboard()

    #
    #  now process the command line arguments 
    #

    for arg in argv:
        if arg.startswith('-'):
            ch = arg[1]
            # switch(argv[i][1]) {
            if ch == 's':       # /* show scoreboard   */
                showscores()
                sys.exit(EXIT_SUCCESS)

            if ch == 'l':       # /* show log file     */
                diedlog()
                sys.exit(EXIT_SUCCESS)

            if ch == 'i':       # /* show all scoreboard */
                showallscores()
                sys.exit(EXIT_SUCCESS)

            if ch == 'c':       #/*anyone with password can create scoreboard*/
                lprcat("Preparing to initialize the scoreboard.\n")
                if getpassword() != 0:  # make new scoreboard
                    makeboard()
                    lprc('\n')
                    showscores()
                sys.exit(EXIT_SUCCESS)

            if ch in '0123456789':  # /* for hardness */
                hard = int(arg[1:])
                continue

            if ch in 'h?':          # /* print out command line arguments */
                print(cmdhelp)
                sys.exit(EXIT_SUCCESS)

            # default:
            print("Unknown option <{}>".format(arg))
            print(cmdhelp, end='')
            sys.exit(EXIT_SUCCESS)

    userid = getplid(logname)       # /* obtain the players id number */

    if userid < 0:
        print("Can't optain playerid", file=sys.stderr)
        sys.exit(EXIT_SUCCESS)      # FIXME: EXIT_FAILURE.

    #
    #  He really wants to play, so malloc the memory for the dungeon.
    #

    try:
        cell = [struct_cel()] *  ((MAXLEVEL + MAXVLEVEL) * MAXX * MAXY)
    except MemoryError as err:
        # /* malloc failure */
        died(-285)

    
    lcreat(None)                    # Open terminal for output
    newgame()                       # /*  set the initial clock  */

    if os.access(savefilename, os.F_OK):
                                    # /* restore game if need to */
        clear()
        restorflag = 1
        hitflag = 1
        restoregame(savefilename)   # /* restore last game    */

    setupvt100()                    # /* setup the terminal special mode */
    sethard(hard)                   # /* set up the desired difficulty */

    if c[HP] == 0:                  # /* create new game */
        # /* tell signals that we are in the welcome screen */
        predostuff = 1
        welcome()                   # /* welcome the player to the game */
        makeplayer()                # /* make the character that will play */
        newcavelevel(0)             # /* make the dungeon */
        # /* Display their mail if they've just won the previous game */
        checkmail()

    lprc(T_INIT)                    # /* Reinit the screen because of welcome 
                                    #    and check mailhaving embedded escape 
                                    #    sequences. */
    drawscreen()                    # /*  show the initial dungeon */
    
    # /* tell the trap functions that they must do a showplayer() from here on */
    predostuff = 2
    yrepcount = hit2flag = 0
    # 
    #  init previous player position to be current position, so we don't
    #  reveal any stuff on the screen prematurely.
    #
    oldx = playerx
    oldy = playery
    gtime = -1

    # 
    # MAINLOOP
    #  find objects, move stuff, get commands, regenerate
    #
    while True:
        if dropflag == 0:
            # /* see if there is an object here.
            #
            #    If in prompt mode, identify and prompt; else
            #    identify, never prompt.
            # */
            lookforobject(True, False, False)
        else:
            dropflag = 0            # /* don't show it just dropped an item */

        # /* handle global activity
        #    update game time, move spheres, move walls, move monsters
        #    all the stuff affected by TIMESTOP and HASTESELF
        # */
        if c[TIMESTOP] <= 0:
            if c[HASTESELF] == 0 or c[HASTESELF] & 1 == 0:
                gtime += 1
                movsphere()

                if hitflag == 0:
                    if c[HASTEMONST]:
                        movemonst()
                    movemonst()
        #
        # /* show stuff around the player */
        #
        if viewflag == 0:
            showcell(playerx, playery)
        else:
            viewflag = 0

        if hit3flag:
            lflushall()

        hitflag = hit3flag = 0
        bot_linex()                 # /* update bottom line */

        #
        # /* get commands and make moves */
        #
        nomove = 1
        while nomove:
            if hit3flag:
                lflushall()
            nomove = 0
            parse()

        regen()                     # /*  regenerate hp and spells */
        if c[TIMESTOP] == 0:
            rmst -= 1
            if rmst <= 0:
                rmst = 120 - (level << 2)
                fillmonst(makemonst(level))

    return EXIT_SUCCESS


if __name__ == '__main__':
    sys.exit(main(sys.argv))

"""
static void        parse(void);
static void        randmonst(void);
static void        run(int);
static void        wield(void);
static void        ydhi(int);
static void        ycwi(int);
static void        wear(void);
static void        dropobj(void);
static int        floor_consume(int, char *);
static void        consume(int, char *, int (*)());
static int        whatitem(char *);






/*
 * subroutine to randomly create monsters if needed
 */
static void randmonst(void)
{

    /*  don't make monsters if time is stopped  */
    if (c[TIMESTOP]) {
        
        return;
    }
    
    if (--rmst <= 0) {

        rmst = 120 - (level<<2);
        
        fillmonst(makemonst(level));
        }
}



/*
 * parse()
 *
 * get and execute a command
 */
static void parse(void)
{
    int i, j, k, flag;

    while   (1)
        {
        k = yylex();
        switch(k)   /*  get the token from the input and switch on it   */
            {
            case 'h':   moveplayer(4);  return;     /*  west        */
            case 'H':   run(4);         return;     /*  west        */
            case 'l':   moveplayer(2);  return;     /*  east        */
            case 'L':   run(2);         return;     /*  east        */
            case 'j':   moveplayer(1);  return;     /*  south       */
            case 'J':   run(1);         return;     /*  south       */
            case 'k':   moveplayer(3);  return;     /*  north       */
            case 'K':   run(3);         return;     /*  north       */
            case 'u':   moveplayer(5);  return;     /*  northeast   */
            case 'U':   run(5);         return;     /*  northeast   */
            case 'y':   moveplayer(6);  return;     /*  northwest   */
            case 'Y':   run(6);         return;     /*  northwest   */
            case 'n':   moveplayer(7);  return;     /*  southeast   */
            case 'N':   run(7);         return;     /*  southeast   */
            case 'b':   moveplayer(8);  return;     /*  southwest   */
            case 'B':   run(8);         return;     /*  southwest   */

            case '.':                               /*  stay here       */
                if (yrepcount) 
                    viewflag=1;
                return;

            case 'c':
                yrepcount=0;
                cast();
                return;     /*  cast a spell    */

            case 'd':
                yrepcount=0;
                if (c[TIMESTOP]==0)
                    dropobj();
                return; /*  to drop an object   */

            case 'e':
                yrepcount=0;
                if (c[TIMESTOP]==0)
                    if (!floor_consume( OCOOKIE, "eat" ))
                        consume( OCOOKIE, "eat", showeat );
                return; /*  to eat a fortune cookie */

            case 'g':   
                yrepcount = 0 ;
                cursors();
                lprintf("\nThe stuff you are carrying presently weighs %d pounds",(long)packweight());
                break ;

            case 'i':       /* inventory */
                yrepcount=0;
                nomove=1;
                showstr(FALSE);
                return;

            case 'p':           /* pray at an altar */
                yrepcount = 0;
                    pray_at_altar();
                return;

            case 'q':           /* quaff a potion */
                yrepcount=0;
                if (c[TIMESTOP]==0)
                    if (!floor_consume( OPOTION, "quaff"))
                        consume( OPOTION, "quaff", showquaff );
                return;

            case 'r':
                yrepcount=0;
                if (c[BLINDCOUNT])
                    {
                    cursors();
                    lprcat("\nYou can't read anything when you're blind!");
                    }
                else if (c[TIMESTOP]==0)
                    if (!floor_consume( OSCROLL, "read" ))
                        if (!floor_consume( OBOOK, "read" ))
                            consume( OSCROLL, "read", showread );
                return;     /*  to read a scroll    */

            case 's':
                yrepcount = 0 ;
                    sit_on_throne();
                return ;

            case 't':                       /* Tidy up at fountain */
                yrepcount = 0 ;
                    wash_fountain() ;
                return ;

            case 'v':
                yrepcount=0;
                nomove = 1;
                cursors();
                lprintf("\nLarn, Version %d.%d.%d, Diff=%d",(long)VERSION,(long)SUBVERSION,(long)PATCHLEVEL,(long)c[HARDGAME]);
                if (wizard)
                    lprcat(" Wizard");
                if (cheat) 
                    lprcat(" Cheater");
                return;

            case 'w':                       /*  wield a weapon */
                yrepcount=0;
                wield();
                return;

            case 'A':
                yrepcount = 0;
                    desecrate_altar();
                return;

            case 'C':                       /* Close something */
                yrepcount = 0 ;
                    close_something();
                return;

            case 'D':                       /* Drink at fountain */
                yrepcount = 0 ;
                    drink_fountain() ;
                return ;

            case 'E':               /* Enter a building */
                yrepcount = 0 ;
                    enter() ;
                break ;

            case 'I':              /*  list spells and scrolls */
                yrepcount=0;
                seemagic(0);
                nomove=1;
                return;

            case 'O':               /* Open something */
                yrepcount = 0 ;
                    open_something();
                return;

            case 'P':
                cursors();
                yrepcount = 0;
                nomove = 1;
                if (outstanding_taxes>0)
                    lprintf("\nYou presently owe %d gp in taxes.",(long)outstanding_taxes);
                else
                    lprcat("\nYou do not owe any taxes.");
                return;

            case 'Q':    /*  quit        */
                yrepcount=0;
                quit();
                nomove=1;
                return;

            case 'R' :          /* remove gems from a throne */
                yrepcount = 0 ;
                    remove_gems( );
                return ;

            case 'S':
                /* And do the save.
                 */
                cursors();
                lprintf("\nSaving to `%s' . . . ", savefilename);
                lflush();
                save_mode = 1;
                savegame(savefilename);
                clear();
                lflush();
                wizard=1;
                died(-257); /* doesn't return */
                break;


            case 'T':   yrepcount=0;    cursors();  if (c[SHIELD] != -1) { c[SHIELD] = -1; lprcat("\nYour shield is off"); bottomline(); } else
                                        if (c[WEAR] != -1) { c[WEAR] = -1; lprcat("\nYour armor is off"); bottomline(); }
                        else lprcat("\nYou aren't wearing anything");
                        return;

            case 'W':
                yrepcount=0;
                wear();
                return; /*  wear armor  */

            case 'Z':
                yrepcount=0;
                if (c[LEVEL]>9) 
                    { 
                    oteleport(1);
                    return; 
                    }
                cursors(); 
                lprcat("\nAs yet, you don't have enough experience to use teleportation");
                return; /*  teleport yourself   */

            case ' ':   yrepcount=0;    nomove=1;  return;

            case 'L'-64:  yrepcount=0;  drawscreen();  nomove=1; return;    /*  look        */

#if WIZID
#ifdef EXTRA
            case 'A'-64:    yrepcount=0;    nomove=1; if (wizard) { diag(); return; }  /*   create diagnostic file */
                        return;
#endif
#endif
        
        case '<':                       /* Go up stairs or vol shaft */
                yrepcount = 0;
                    up_stairs();
                return ;

            case '>':                       /* Go down stairs or vol shaft*/
                yrepcount = 0 ;
                    down_stairs();
                return ;

            case '?':                       /* give the help screen */
                yrepcount=0;
                help();
                nomove=1;
                return; 

        case ',':                       /* pick up an item */
            yrepcount = 0 ;
            /* pickup, don't identify or prompt for action */
            lookforobject( FALSE, TRUE, FALSE );
        return;

            case ':':                       /* look at object */
                yrepcount = 0 ;
            /* identify, don't pick up or prompt for action */
                    lookforobject( TRUE, FALSE, FALSE );
                nomove = 1;  /* assumes look takes no time */
                return;

        case '/':        /* identify object/monster */
            specify_object();
            nomove = 1 ;
            yrepcount = 0 ;
            return;

        case '^':                       /* identify traps */
                flag = yrepcount = 0;
                cursors();
                lprc('\n');
                for (j=playery-1; j<playery+2; j++)
                    {
                    if (j < 0)
                        j=0;
                    if (j >= MAXY)
                        break;
                    for (i=playerx-1; i<playerx+2; i++)
                        {
                        if (i < 0) 
                            i=0;
                        if (i >= MAXX) 
                            break;
                        switch(item[i][j])
                            {
                            case OTRAPDOOR:     case ODARTRAP:
                            case OTRAPARROW:    case OTELEPORTER:
                            case OPIT:
                                lprcat("\nIts ");
                                lprcat(objectname[item[i][j]]);
                                flag++;
                            };
                        }
                    }
                if (flag==0) 
                    lprcat("\nNo traps are visible");
                return;

#if WIZID
            case '_':   /*  this is the fudge player password for wizard mode*/
                        yrepcount=0;    cursors(); nomove=1;

                        if (getpassword()==0)
                            {
                            scbr(); /* system("stty -echo cbreak"); */ return;
                            }
                        wizard=1;  scbr(); /* system("stty -echo cbreak"); */
                        for (i=0; i<6; i++)  c[i]=70;  iven[0]=iven[1]=0;
                        take(OPROTRING,50);   take(OLANCE,25);  c[WIELD]=1;
                        c[LANCEDEATH]=1;   c[WEAR] = c[SHIELD] = -1;
                        raiseexperience(6000000L);  c[AWARENESS] += 25000;
                        {
                        int i,j;
                        for (i=0; i<MAXY; i++)
                            for (j=0; j<MAXX; j++)  know[j][i]=KNOWALL;
                        for (i=0; i<SPNUM; i++) spelknow[i]=1;
                        for (i=0; i<MAXSCROLL; i++)  scrollname[i][0]=' ';
                        for (i=0; i<MAXPOTION; i++)  potionname[i][0]=' ';
                        }
                        for (i=0; i<MAXSCROLL; i++)
                          if (strlen(scrollname[i])>2) /* no null items */
                            { item[i][0]=OSCROLL; iarg[i][0]=i; }
                        for (i=MAXX-1; i>MAXX-1-MAXPOTION; i--)
                          if (strlen(potionname[i-MAXX+MAXPOTION])>2) /* no null items */
                            { item[i][0]=OPOTION; iarg[i][0]=i-MAXX+MAXPOTION; }
                        for (i=1; i<MAXY; i++)
                            { item[0][i]=i; iarg[0][i]=0; }
                        for (i=MAXY; i<MAXY+MAXX; i++)
                            { item[i-MAXY][MAXY-1]=i; iarg[i-MAXY][MAXY-1]=0; }
            for (i=MAXX+MAXY; i<MAXOBJECT; i++)
                {
                item[MAXX-1][i-MAXX-MAXY]=i;
                iarg[MAXX-1][i-MAXX-MAXY]=0;
                }
                        c[GOLD]+=250000;    drawscreen();   return;
#endif

            };
        }
}



void parse2(void)
{

    /* move the monsters */
    if (c[HASTEMONST]) {

        movemonst();
    }
    
    movemonst(); 
    
    randmonst();

    regen();
}

    
    
static void run(int dir)
{
    int i;
    
    i = 1; 

    while (i) {
        
        i = moveplayer(dir);
        
        if (i > 0) {

            if (c[HASTEMONST]) {
                
                movemonst();
            }
            
            movemonst();
            randmonst();
            regen();
        }
        
        if (hitflag) {

            i = 0;
        }
        
        if (i != 0) {

            showcell(playerx,playery);
        }
    }
}



/*
 * function to wield a weapon
 */
static void wield(void)
{
    int i;

    while (TRUE) {
        
        i = whatitem("wield (- for nothing)");
        if (i == '\33') return;
        
        
        if (i != '.') {
            
            if (i == '*') {
                
                i = showwield();
                cursors();
            }
        
            if ( i == '-' ) {
                
                c[WIELD] = -1 ;
                bottomline();
                
                return;
            }
            
            if (!i || i == '.') {
        
                continue;
            }

            if (iven[i-'a']==0) { 
                    
                ydhi(i);
                return;
                    
            } else if (iven[i - 'a'] == OPOTION) { 
                    
                ycwi(i); 
                return;
                    
            } else if (iven[i-'a'] == OSCROLL) {
                    
                ycwi(i);
                return;
                    
            } else if (c[SHIELD] != -1 &&
                iven[i-'a'] == O2SWORD) {
                        
                lprcat("\nBut one arm is busy with your shield!");
                return;
                        
            } else {
            
                c[WIELD]= i - 'a';
                    
                if (iven[i - 'a'] == OLANCE) {
                        
                    c[LANCEDEATH]=1;
                        
                } else {
                        
                    c[LANCEDEATH]=0;
                }
                    
                bottomline();
                return;
            }
        }
    }
}

    

/*
 * common routine to say you don't have an item
 */
static void ydhi(int x)
{

    cursors();
    
    lprintf("\nYou don't have item %c!",x);
}



/*
 * common routine to say you can't wield an item
 */   
static void ycwi(int x)
{
    cursors();
    
    lprintf("\nYou can't wield item %c!",x);
}



/*
    function to wear armor
 */
static void wear(void)
{
    int i;
    
    while (1)
        {
        if ((i = whatitem("wear"))=='\33')
            return;
        if (i != '.' && i != '-')
            {
            if (i=='*')
                {
                i = showwear();
                cursors();
                }
            if (i && i != '.')
                switch(iven[i-'a'])
                    {
                    case 0:
                        ydhi(i);
                        return;
                    case OLEATHER:  case OCHAIN:  case OPLATE:
                    case ORING:     case OSPLINT: case OPLATEARMOR:
                    case OSTUDLEATHER:            case OSSPLATE:
                        if (c[WEAR] != -1) { lprcat("\nYou're already wearing some armor"); return; }
                            c[WEAR]=i-'a';  bottomline(); return;
                    case OSHIELD:   if (c[SHIELD] != -1) { lprcat("\nYou are already wearing a shield"); return; }
                                if (iven[c[WIELD]]==O2SWORD) { lprcat("\nYour hands are busy with the two handed sword!"); return; }
                                c[SHIELD] = i-'a';  bottomline(); return;
                    default:    lprcat("\nYou can't wear that!");
                    };
            }
        }
}




/*
    function to drop an object
 */
static void dropobj(void)
{
    int i;
    signed char *p;
    unsigned long amt;

    p = &item[playerx][playery];
    while (1)
        {
        if ((i = whatitem("drop"))=='\33')
        return;
    if (i=='*')
        {
        i = showstr(TRUE);
        cursors();
        }
    if ( i != '-' )
            {
            if (i=='.') /* drop some gold */
                {
                if (*p) { lprcat("\nThere's something here already!"); return; }
                lprcat("\n\n");
                cl_dn(1,23);
                lprcat("How much gold do you drop? ");
                if ((amt=readnum((long)c[GOLD])) == 0) return;
                if (amt>c[GOLD])
                    {
            lprcat("\n");
            lprcat("You don't have that much!");
            return; }
                if (amt<=32767)
                    { *p=OGOLDPILE; i=amt; }
                else if (amt<=327670L)
                    { *p=ODGOLD; i=amt/10; amt = 10L*i; }
                else if (amt<=3276700L)
                    { *p=OMAXGOLD; i=amt/100; amt = 100L*i; }
                else if (amt<=32767000L)
                    { *p=OKGOLD; i=amt/1000; amt = 1000L*i; }
                else
                    { *p=OKGOLD; i=32767; amt = 32767000L; }
                c[GOLD] -= amt;

                lprintf("\nYou drop %d gold pieces",(long)amt);

                iarg[playerx][playery]=i; bottomgold();
                know[playerx][playery]=0; dropflag=1;  return;
                }
        if (i)
        {
        drop_object(i-'a');
        return;
        }
            }
        }
}


static int floor_consume(int search_item, char *cons_verb)
{
    int i;
    char tempc;

    cursors();
    i = item[playerx][playery];

    /* item not there, quit
    */
    if (i != search_item)
        return( 0 );

    /* item there.  does the player want to consume it?
    */
    lprintf("\nThere is %s", objectname[i] );
    if (i==OSCROLL)
        if (scrollname[iarg[playerx][playery]][0])
            lprintf(" of%s", scrollname[iarg[playerx][playery]]);
    if (i==OPOTION)
        if (potionname[iarg[playerx][playery]][0])
            lprintf(" of%s", potionname[iarg[playerx][playery]]);
    lprintf(" here.  Do you want to %s it?", cons_verb );

    if ((tempc = getyn()) == 'n' )
        return( 0 );                /* item there, not consumed */
    else if (tempc != 'y')
        {
        lprcat(" aborted");
        return( -1 );               /* abort */
        }

    /* consume the item.
    */
    switch( i )
        {
        case OCOOKIE:
            outfortune();
            forget();
            break;
        case OBOOK:
            readbook( iarg[playerx][playery] );
            forget();
            break;
        case OPOTION:
            quaffpotion(iarg[playerx][playery], 1);
            forget();
            break;
        case OSCROLL:
            /* scrolls are tricky because of teleport.
            */
            i = iarg[playerx][playery];
            know[playerx][playery] = 0;
            item[playerx][playery] = iarg[playerx][playery] = 0 ;
            read_scroll( i );
            break;
        }
    return( 1 );
}



static void consume(int search_item, char *prompt, int (*showfunc)())
{
    int i;

    while (1)
        {
        if ((i = whatitem( prompt )) == '\33')
            return;
        if (i != '.' && i != '-')
            {
            if (i == '*')
                {
                i = showfunc();
                cursors();
                }
            if (i && i != '.')
                {
                switch (iven[i-'a'])
                    {
                    case OSCROLL:
                        if ( search_item != OSCROLL )
                            {
                            lprintf("\nYou can't %s that.", prompt );
                            return;
                            }
                        read_scroll( ivenarg[i-'a'] );
                        break;
                    case OBOOK:
                        if ( search_item != OSCROLL )
                            {
                            lprintf("\nYou can't %s that.", prompt );
                            return;
                            }
                        readbook( ivenarg[i-'a'] );
                        break;
                    case OCOOKIE:
                        if ( search_item != OCOOKIE )
                            {
                            lprintf("\nYou can't %s that.", prompt );
                            return;
                            }
                        outfortune();
                        break;
                    case OPOTION:
                        if ( search_item != OPOTION )
                            {
                            lprintf("\nYou can't %s that.", prompt );
                            return;
                            }
                        quaffpotion( ivenarg[i-'a'], TRUE );
                        break;
                    case 0:
                        ydhi(i);
                        return;
                    default:
                        lprintf("\nYou can't %s that.", prompt );
                        return;
                    }
                iven[i-'a'] = 0;
                return;
                }
            }
        }
}



/*
    function to ask what player wants to do
 */
static int whatitem(char *str)
{
    int i=0;

    cursors();  lprintf("\nWhat do you want to %s [* for all] ? ",str);
    while (i>'z' || (i<'a' && i!='-' && i!='*' && i!='\33' && i!='.'))
        i=ttgetch();
    if (i=='\33')
        lprcat(" aborted");
    
    return(i);
}




/*
    subroutine to get a number from the player
    and allow * to mean return amt, else return the number entered
 */
unsigned long readnum(long mx)
{
    int i;
    unsigned long amt=0;

    sncbr();
    /* allow him to say * for all gold 
    */
    if ((i=ttgetch()) == '*')
        amt = mx;
    else
        /* read chars into buffer, deleting when requested */
    while (i != '\n')
        {
        if (i=='\033') { scbr(); lprcat(" aborted"); return(0); }
        if ((i <= '9') && (i >= '0') && (amt<999999999))
            amt = amt*10+i-'0';
        if ((i=='\010') || (i=='\177'))
            amt = (long)(amt / 10) ;
        i = ttgetch();
        }
    scbr();
    return(amt);
}
"""
