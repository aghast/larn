""" /* io.c
     *
     *  setupvt100()    Subroutine to set up terminal in correct mode for game
     *  clearvt100()    Subroutine to clean up terminal when the game is over
     *  ttgetch()       Routine to read in one character from the terminal
     *  scbr()          Function to set cbreak -echo for the terminal
     *  sncbr()         Function to set -cbreak echo for the terminal
     *  newgame()       Subroutine to save the initial time and seed rnd()
     *
     *  FILE OUTPUT ROUTINES
     *
     *  lprintf(format,args . . .)  printf to the output buffer
     *  lprint(integer)         send binary integer to output buffer
     *  lwrite(buf,len)         write a buffer to the output buffer
     *  lprcat(str)         sent string to output buffer
     *
     *  FILE OUTPUT MACROS
     *
     *  lprc(character)         put the character into the output buffer
     *
     *  FILE INPUT ROUTINES
     *
     *  long lgetc()            read one character from input buffer
     *  long larint()            read one integer from input buffer
     *  lrfill(address,number)      put input bytes into a buffer
     *  char *lgetw()           get a whitespace ended word from input
     *  char *lgetl()           get a \n or EOF ended line from input
     *
     *  FILE OPEN / CLOSE ROUTINES
     *
     *  lcreat(filename)        create a new file for write
     *  lopen(filename)         open a file for read
     *  lappend(filename)       open for append to an existing file
     *  lrclose()           close the input file
     *  lwclose()           close output file
     *  lflush()            flush the output buffer
     *
     *  Other Routines
     *
     *  cursor(x,y)     position cursor at [x,y]
     *  cursors()       position cursor at [1,24] (saves memory)
     *  cl_line(x,y)            Clear line at [1,y] and leave cursor at [x,y]
     *  cl_up(x,y)          Clear screen from [x,1] to current line.
     *  cl_dn(x,y)      Clear screen from [1,y] to end of display. 
     *  lstandout(str)       Print the string in standout mode.
     *  set_score_output()  Called when output should be literally printed.
     ** ttputch(ch)     Print one character in decoded output buffer.
     ** flush_buf()     Flush buffer with decoded output.
     ** init_term()     Terminal initialization
     ** char *tmcapcnv(sd,ss)   Routine to convert VT100 \33's to termcap format
     *
     * Note: ** entries are available only in termcap mode.
     */
    #include <stdlib.h>
    #include <stdio.h>
    #include <stdarg.h>
    #include <time.h>
    #include <ctype.h>

    #include <setjmp.h>
    #include <fcntl.h>     /* For O_BINARY */
    #include <conio.h>

    #include "larncons.h"
    #include "larndata.h"
    #include "larnfunc.h"

    #include "ansiterm.h"
    """

import time

from aghast.util import *

from .ansiterm import *
from .larncons import *
from .larndata import *
from .larnfunc import *


lfd :int = 0            # output file numbers
export('lfd')

fd :int = 0             # input file numbers
export('fd')


static()
ipoint: int = MAXIBUF

static()
iepoint: int = MAXIBUF
""" Input buffering pointers. """

static()
LINBUFSIZE :int = 128   # size of the lgetw() and lgetl() buffer 

static()
lgetwbuf: List[str]     # LINBUFSIZE
""" Get line (word) buffer """

static()
getchfn: Callable[[], int] = None

@export
def setupvt100() -> None:
    """ Set up terminal in correct mode for game

        Attributes off, clear screen, set scrolling region, set tty mode.
    """
    clear()
    setscroll()
    scbr()      # system("stty cbreak -echo");

@export
def clearvt100() -> None:
    """ Clean up terminal when the game is over

        Attributes off, clear screen, unset scrolling region, restore tty mode 
    """
    ansiterm_clean_up()
    resetscroll()
    clear()
    sncbr()     # system("stty -cbreak echo");

@export
def ttgetch() -> str:
    """ Read in one character from the terminal."""

    if EXTRA:
        global c
        c.bytesin += 1

    lflush()        # Be sure output buffer is flushed
    byt = getchfn()

    if byt == '\r':
        byt = '\n'

    return byt

@export
def scbr() -> None:
    """ Set cbreak -echo for the terminal.

        Like `system("stty cbreak -echo")`
    """

    # Set up to use the direct console input call which may read from the
    # keypad
    global getchfn
    getchfn = ansiterm_getch

@export
def sncbr() -> None:
    """ Set -cbreak echo for the terminal

        Like: system("stty -cbreak echo")
    """
    # Set up to use the direct console input call with echo, getche()
    global getchfn
    getchfn = ansiterm_getche

@export
def newgame() -> None:
    """ Save the initial time and seed rnd() """

    global c
    for i in range(100):
        c[i] = 0
	
    global initialtime
    initialtime = trunc(time.time())
	srand(initialtime)
	lcreat(0)        # open buffering for output to terminal 

@export
lprintf(format:str, *args: Any) -> None:
    """ Printf to the output buffer.

        Enter with the format string in "format", as per printf() usage and any
        needed arguments following it

        Note: lprintf() only supports %s, %c and %d, with width modifier and
        left or right justification.  No correct checking for output buffer
        overflow is done, but flushes are done beforehand if needed.  
    """
    buffer = format % args

    for ch in buffer:
        lprc(ch)

@export
lprint(longint:int) -> None:
    """ Send binary integer to output buffer.

        +---------+---------+---------+---------+
        |   high  |         |         |   low   |
        |  order  |         |         |  order  |
        |   byte  |         |         |   byte  |
        +---------+---------+---------+---------+
        31 ---- 24 23 --- 16 15 ---- 8 7 ------ 0
        
        The save order is low order first, to high order (4 bytes total) and
        is written to be system independent.  No checking for output buffer
        overflow is done, but flushes if needed!
    """

    if lpnt >= lpend - 4:
        lflush()
    
    lpbuf[lpnt] = 255 & longint
    lpnt += 1
    lpbuf[lpnt] = 255 & (longint >> 8)
    lpnt += 1
	lpbuf[lpnt] = 255 & (longint >> 16)
    lpnt += 1
    lpbuf[lpnt] = 255 & (longint >> 24)
    lpnt += 1
}

@export
def lprc(ch: str) -> None:
    """ Output one byte to the output buffer. """

    lpbuf[lpnt] = ch
    lpnt += 1

    if lpnt >= lpend:
        lflush()

@export
def lwrite(buf:str, buflen:int) -> None:
    """ Write a buffer to the output buffer.

        Enter with the address and number of bytes to write out
    """
    if EXTRA:
        global c
        c.bytesout += buflen

    # FIXME: Could manipulate the buffer directly, if it's worth coding.
    lprc_ = lprc
    for ch in buf[:buflen]:
        lprc_(ch)

@export 
def lgetc() -> str:
    """ Read one character from input buffer.

        Returns "" if EOF, otherwise the character.
    """

    global ipoint
    if ipoint != iepoint:
        ch = inbuffer[ipoint]
        ipoint += 1
        return ch

    if iepoint != MAXIBUF:
        return 0

    global inbuffer
    global fd
    try:
        inbuffer = fd.read(MAXIBUF)
    except OSError:
        print("error reading from input file")
        iepoint = ipoint = 0
        return ""

    if len(inbuffer):
        ipoint = 1
        iepoint = len(inbuffer)
        return inbuffer[0]

    return ""

@export
def larint() -> int:
    """ Read one integer from input buffer 

        +---------+---------+---------+---------+
        |   high  |         |         |   low   |
        |  order  |         |         |  order  |
        |   byte  |         |         |   byte  |
        +---------+---------+---------+---------+
       31  ---  24 23 --- 16 15 ---  8 7  ---   0
    
        The save order is low order first, to high order (4 bytes total)
        Returns the int read
    """
    i :int = 0
    i = 255 & lgetc()
    i |= (255 & lgetc()) << 8
    i |= (255 & lgetc()) << 16
    i |= (255 & lgetc()) << 24
    return i


"""
===========================================================================
                    C SOURCE CODE BELOW THIS POINT
===========================================================================


/*
 *  lrfill(address,number)          put input bytes into a buffer
 *      char *address;
 *      int number;
 *
 *  Reads "number" bytes into the buffer pointed to by "address".
 *  Returns nothing of value
 */
void lrfill(char * adr, int num)
{
	char *pnt;
	int num2;

    while (num)
        {
        if (iepoint == ipoint)
            {
            if (num>5) /* fast way */
                {
                if (read(fd,adr,num) != num)
                    write(2,"error reading from input file\n",30);
                num=0;
                }
            else { *adr++ = lgetc();  --num; }
            }
        else
            {
            num2 = iepoint-ipoint;  /*  # of bytes left in the buffer   */
            if (num2 > num) num2=num;
            pnt = inbuffer+ipoint;  num -= num2;  ipoint += num2;
            while (num2--)  *adr++ = *pnt++;
            }
        }
}



/*
 *  char *lgetw()           Get a whitespace ended word from input
 *
 *  Returns pointer to a buffer that contains word.  If EOF, returns a NULL
 */
char * lgetw(void)
{
	char *lgp, cc;
	int n = LINBUFSIZE, quote = 0;

    lgp = lgetwbuf;
    do cc=lgetc();  while ((cc <= 32) && (cc > '\0'));  /* eat whitespace */
    for ( ; ; --n,cc=lgetc())
        {
        if ((cc== '\0') && (lgp==lgetwbuf))  return(NULL);   /* EOF */
        if ((n<=1) || ((cc<=32) && (quote==0))) { 
		*lgp= '\0';
		return lgetwbuf; 
	}
        if (cc != '"') *lgp++ = cc;   else quote ^= 1;
        }
}



/*
 *  char *lgetl()       Function to read in a line ended by newline or EOF
 *
 *  Returns pointer to a buffer that contains the line.  If EOF, returns NULL
 */
char * lgetl(void)
{
	int i = LINBUFSIZE, ch;
	char *str = lgetwbuf;

    for ( ; ; --i) {
        *str++ = ch = lgetc();
        if (ch == 0) {
            if (str == lgetwbuf+1)
                return(NULL);   /* EOF */
        ot: *str = 0;
            return(lgetwbuf);   /* line ended by EOF */
        }
        if ((ch=='\n') || (i<=1))
            goto ot;        /* line ended by \n */
    }
}



/*
 *  lcreat(filename)            Create a new file for write
 *      char *filename;
 *
 *  lcreat((char*)0); means to the terminal
 *  Returns -1 if error, otherwise the file descriptor opened.
 */
int lcreat(char *str)
{
    lpnt = lpbuf;   lpend = lpbuf+BUFBIG;
    if (str==NULL) return(lfd=1);
    if ((lfd=creat(str,0644)) < 0) 
        {
        lfd=1; lprintf("error creating file <%s>\n",str); lflush(); return(-1);
        }

    setmode(lfd, O_BINARY);

    return lfd;
}



/*
 *  lopen(filename)         Open a file for read
 *      char *filename;
 *
 *  lopen(0) means from the terminal
 *  Returns -1 if error, otherwise the file descriptor opened.
 */
int lopen(char *str)
{
	ipoint = iepoint = MAXIBUF;
	
	if (str==NULL) return(fd=0);

	if ((fd=open(str,0)) < 0)
        {
        lwclose(); lfd=1; lpnt=lpbuf; return(-1);
        }

    setmode(fd, O_BINARY);

	return fd;
}
    


/*
 *  lappend(filename)       Open for append to an existing file
 *      char *filename;
 *
 *  lappend(0) means to the terminal
 *  Returns -1 if error, otherwise the file descriptor opened.
 */
int lappend(char *str)
{
    lpnt = lpbuf;   lpend = lpbuf+BUFBIG;
    if (str==NULL) return(lfd=1);
    if ((lfd=open(str,2)) < 0)
        {
        lfd=1; return(-1);
        }

    setmode(lfd, O_BINARY);

    lseek(lfd,0L,2);    /* seek to end of file */
    
	return lfd;
}



/*
 *  lrclose()                       close the input file
 *
 *  Returns nothing of value.
 */
void lrclose(void)
{

	if (fd > 0) {
		
		close(fd);
	}
}

    

/*
 *  lwclose()                       close output file flushing if needed
 *
 *  Returns nothing of value.
 */
void lwclose(void)
{
	lflush();
	
	if (lfd > 2) {
		
		close(lfd);
	}
}
    
    

/*
 *  lprcat(string)                  append a string to the output buffer
 *                                  avoids calls to lprintf (time consuming)
 */
void lprcat(char *str)
{
	char *str2;
	
	if (lpnt >= lpend) {
		
		lflush();
	}
	
	str2 = lpnt;
	
	while ((*str2++ = *str++) != '\0') 
		;
	
	lpnt = str2 - 1;
}



/*
 * cursor(x,y)    Put cursor at specified coordinates staring at [1,1] (termcap)
 */
void cursor(int x, int y)
{
	
	if (lpnt >= lpend) {
		
		lflush ();
	}

	*lpnt++ = CURSOR;
	*lpnt++ = x;
	*lpnt++ = y;
}



/*
 *  Routine to position cursor at beginning of 24th line
 */
void cursors(void)
{

	cursor(1, 24);
}



/*
 * Warning: ringing the bell is control code 7. Don't use in defines.
 * Don't change the order of these defines.
 * Also used in helpfiles. Codes used in helpfiles should be \E[1 to \E[7 with
 * obvious meanings.
 */

/* translated output buffer */
static char *	outbuf = NULL;  

    
/*
 * ANSI control sequences
 */

/* clear to end of line */
static const char CE[] = {27, '[', 'K', 0};

/* clear to end of display */
static char *CD = NULL; 

/* clear screen */
static const char CL[] = {27, '[', ';', 'H', 27, '[', '2', 'J', 0};

/* cursor motion */
static const char CM[] = {27, '[', '%', 'i', '%', '2', ';', '%', '2', 'H', 0};

/* insert line */
static const char AL[] = {27, '[', 'L', 0};

/* delete line */
static const char DL[] = {27, '[', 'M', 0};

/* begin standout mode */
static const char SO[] = {27, '[', '1', 'm', 0};

/* end standout mode */
static const char SE[] = {27, '[', 'm', 0};

/* terminal initialization */
static const char TI[] = {27, '[', 'm', 0};

/* terminal end */
static const char TE[] = {27, '[', 'm', 0};




static void	ttputch(int);
    
    
/*
 * init_term()      Terminal initialization
 */
void init_term(void)
{

	/* get memory for decoded output buffer*/
	outbuf = malloc(BUFBIG + 16);
	
	if (outbuf == NULL) {

		write(2, "Error malloc'ing memory for decoded" 
			" output buffer\n", 50);

		/* malloc() failure */
		died(-285); 
        }
	
	ansiterm_init();
}


/*
 * cl_line(x,y)  Clear the whole line indicated by 'y' and leave cursor at [x,y]
 */
void cl_line(int x, int y)
{

	cursor(1, y);
	
	*lpnt++ = CL_LINE;

	cursor(x,y);
}



/*
 * cl_up(x,y) Clear screen from [x,1] to current position. Leave cursor at [x,y]
 */
void cl_up(int x, int y)
{
	int i;
	
	cursor(1, 1);
	
	for (i = 1; i <= y; i++) {
		
		*lpnt++ = CL_LINE;
		*lpnt++ = '\n';
	}
	
	cursor(x,y);
}




/*
 * cl_dn(x,y)   Clear screen from [1,y] to end of display. Leave cursor at [x,y]
 */
void cl_dn(int x, int y)
{
	int i;
	
	cursor(1, y);
	
	if (CD == NULL) {

		*lpnt++ = CL_LINE;
		
		for (i=y; i<=24; i++) {
			
			*lpnt++ = CL_LINE;
			
			if (i!=24) *lpnt++ = '\n';
		}
		
		cursor(x,y);

        } else {
		
		*lpnt++ = CL_DOWN;
	}
    
	cursor(x,y);
}



/*
 * lstandout(str)    Print the argument string in inverse video (standout mode).
 */
void lstandout(char *str)
{

	*lpnt++ = ST_START;
	
	while (*str) {

		*lpnt++ = *str++;
	}
		
	*lpnt++ = ST_END;
}



    
/*
 * set_score_output()   Called when output should be literally printed.
 */
void set_score_output(void)
{

	enable_scroll = -1;
}
    
    

/*
 *  lflush()                        Flush the output buffer
 *
 *  Returns nothing of value.
 *  for termcap version: Flush output in output buffer according to output
 *                       status as indicated by `enable_scroll'
 */
static int scrline=18; /* line # for wraparound instead of scrolling if no DL */


void lflush(void)
{
	int lpoint;
	char *str;
	static int curx = 0;
	static int cury = 0;

    if ((lpoint = lpnt - lpbuf) > 0)
        {
#ifdef EXTRA
        c[BYTESOUT] += lpoint;
#endif
        if (enable_scroll <= -1) {
            flush_buf();
		
            /* Catch write errors on save files
             */
                if (write(lfd,lpbuf,lpoint) != lpoint) {
                        warn("Error writing output file\n");
                }

	
            lpnt = lpbuf;   /* point back to beginning of buffer */
            return;
        }
        for (str = lpbuf; str < lpnt; str++)
            {
            if (*str>=32)   { ttputch (*str); curx++; }
            else switch (*str) {
                case CLEAR:     tputs (CL);     curx = cury = 0;
                                break;

                case CL_LINE:   tputs (CE);
                                break;

                case CL_DOWN:   tputs (CD);
                                break;

                case ST_START:  tputs (SO);
                                break;

                case ST_END:    tputs (SE);
                                break;

                case CURSOR:    curx = *++str - 1;      cury = *++str - 1;
                                tputs (atgoto (CM, curx, cury));
                                break;

                case '\n':      
				if ((cury == 23) && enable_scroll) {
					  
					if (++scrline > 23) {
						
						scrline=19;
					}
					
					tputs (atgoto (CM, 0, scrline + 1));
					tputs (CE); 
					
					tputs (atgoto (CM, 0, scrline));
					tputs (CE);
					
				} else {
					
					ttputch ('\n');
					cury++;
				}
				
                                curx = 0;
                                break;
	
                case T_INIT:
                    if (TI)
                        tputs(TI);
                    break;
                case T_END:
                    if (TE)
                        tputs(TE);
                    break;
                default:
                    ttputch (*str);
                    curx++;
                }
            }
        }
    lpnt = lpbuf;
    flush_buf();    /* flush real output buffer now */
}



static int index=0;
    
/*
 * ttputch(ch)      Print one character in decoded output buffer.
 */
static void ttputch(int c)
{

	outbuf[index++] = c;
	
	if (index >= BUFBIG) {
		
		flush_buf();
	}
}



/*
 * Outputs string pointed to by cp
 */
static void tputs(const char *cp)
{

	if (cp == NULL) {

		return;
	} 

	while (*cp != '\0') {

		ttputch(*cp++);
	}
}



/*
 * flush_buf()          Flush buffer with decoded output.
 */
static void flush_buf(void)
{
    if (index) {
	    
	if (lfd == 1) {
	
		ansiterm_out(outbuf, index);

	} else {
		
		write(lfd, outbuf, index);
	}
    }

    index = 0;
}




/*
 *  flushall()  Function to flush all type-ahead in the input buffer
 */
void lflushall(void)
{

	while (kbhit()) {
	    
		getch();
	}
}







/*
 *  char *tmcapcnv(sd,ss)  Routine to convert VT100 escapes to termcap format
 *
 *  Processes only the \33[#m sequence (converts . files for termcap use 
 */
char * tmcapcnv(char *sd, char *ss)  
{
	int tmstate=0; /* 0=normal, 1=\33 2=[ 3=# */
	char tmdigit=0; /* the # in \33[#m */

    while (*ss)
        {
        switch(tmstate)
            {
            case 0: if (*ss=='\33')  { tmstate++; break; }
              ign:  *sd++ = *ss;
              ign2: tmstate = 0;
                    break;
            case 1: if (*ss!='[') goto ign;
                    tmstate++;
                    break;
            case 2: if (isdigit(*ss)) { tmdigit= *ss-'0'; tmstate++; break; }
                    if (*ss == 'm') { *sd++ = ST_END; goto ign2; }
                    goto ign;
            case 3: if (*ss == 'm')
                        {
                        if (tmdigit) *sd++ = ST_START;
                            else *sd++ = ST_END;
                        goto ign2;
                        }
            default: goto ign;
            };
        ss++;
        }
    *sd=0; /* NULL terminator */
    return(sd);
}



static void warn(char *msg)
{

    fprintf(stderr, msg);
}



void enter_name(void)
{
	int c, i;
	
	lprcat("\n\nEnter character name:\n");
	
	sncbr();
	
	i = 0;

	do {
		int c;
		
		c = ttgetch();
	
		if (c == '\n') break;
		
		logname[i] = c;

	} while (++i < LOGNAMESIZE - 1);
	
	logname[i] = '\0';
	
	scbr();
}


void select_sex(void)
{
	int c;
	
	lprcat("\n\nSelect character sex (0=female,1=male):\n");
	
	sncbr();
	
	c = ttgetch();
	
	if (c == '0') {
		
		sex = 0;
		
	} else {
		
		sex = 1;
	}
	
	scbr();
}

"""
