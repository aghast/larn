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

import os
import sys
import time

from aghast.util import export, static

from .ansiterm import *
from .larncons import *
from .larndata import *
from .larnfunc import *


fd :int = 0             # input file numbers
export('fd')            # Used in 2 other places, I believe. diag.c and scores.c


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
    scbr()

@export
def clearvt100() -> None:
    """ Clean up terminal when the game is over

        Attributes off, clear screen, unset scrolling region, restore tty mode 
    """
    ansiterm.clean_up()
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
    getchfn = ansiterm.getch

@export
def sncbr() -> None:
    """ Set -cbreak echo for the terminal

        Like: system("stty -cbreak echo")
    """
    # Set up to use the direct console input call with echo, getche()
    global getchfn
    getchfn = ansiterm.getche

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
def lprintf(format:str, *args: Any) -> None:
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
def lprint(longint:int) -> None:
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

    global inbuffer
    global ipoint
    if ipoint != iepoint:
        ch = inbuffer[ipoint]
        ipoint += 1
        return ch

    if iepoint != MAXIBUF:
        return 0

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

@export
def lrfill(number) -> None:
    """ Fill `buffer` with `number` input bytes read from input `fd`. 
    
        Instead of filling, returns the desired data. Use simple assignment
        or slice assignment to control the data:
            
            So: lrfill(some_buffer, size)
            becomes: some_buffer = lrfill(size)

            And: lrfill(some_buffer + offset, size)
            becomes: some_buffer[offset:] = lrfill(size)

    """
    results = [lgetc() for _ in range(number)]
    return results

@export
def lgetw() -> str:
    """ Get a whitespace ended word from input.

        Returns word, or None if EOF occurs before any characters.
    """
    cc = lgetc()
    in_quotes = False
    word = []

    while cc and cc.isspace():
        # Scan forward over whitespace characters
        cc = lgetc()

    while cc:
        # Accumulate word. Allow spaces inside "quoted strings."
        if cc.isspace() and not in_quotes:
            break

        if cc == '"':
            in_quotes = not in_quotes
        else:
            word.append(cc)

        cc = lgetc()

    word = ''.join(word)
    return word

@export
def lgetl() -> str:
    """ Read in a line terminated by newline (or EOF).

        Returns the line read, or an empty string.
    """

    line = []
    ch = lgetc()

    while ch and ch != '\n':
        line.append(ch)
        ch = lgetc()

    return ''.join(line)

static()
Write_fd :int = 0            # output file numbers

@static
def flush_buf() -> None:
    """ Flush buffer with decoded output. """
    if index:
        if Write_fd == 1:
            ansiterm.out(outbuf, index)
        else:
            write(Write_fd, outbuf, index)

        index = 0

@export
def lappend(filename: str) -> int:
    """ Open for append to an existing file.

        lappend(0) means to the terminal (standard output).

        Returns -1 on error, otherwise the file descriptor opened.
    """

    lpnt = 0
    lpend = BUFBIG

    if not filename:
        Write_fd = 1

    else:
        try:
            Write_fd = open(filename, os.O_APPEND|os.O_BINARY)
            os.lseek(Write_fd, 0, os.SEEK_END)
        except OSError as err:
            Write_fd = 1
            lprintf(f"Error opening file <{filename}> for appending\n")
            lprintf(f"... {str(err)}\n")
            lflush()
            return -1

    return Write_fd

@export
def lcreat(filename: str) -> int:
    """ Create a new file for writing.

        If filename is empty or none,  opens the terminal (stdout).

        Returns -1 on error, otherwise the file descriptor opened.
    """
    global Write_fd

    # TODO: something with these?
    # lpnt = lpbuf
    # lpend = lpbuf + BUFBIG

    if not filename:
        Write_fd = 1

    else:
        try:
            Write_fd = os.open(filename, os.O_BINARY|os.O_WRONLY, mode=0o644)
        except OSError as err:
            Write_fd = 1
            lprintf(f"Error creating file <{filename}>\n")
            lprintf(f"... {str(err)}\n")
            lflush()
            return -1

    return Write_fd

scrline = 18
""" line # for wraparound instead of scrolling if no DL """

@export
def lflush() -> None:
    """ Flush the output buffer.

        For termcap version: Flush output in output buffer according to
        output status as indicated by `enable_scroll`
    """
    lpoint :int = lpnt

    if not hasattr(lflush, 'curx'):
        # static int curx = 0, cury = 0;
        lflush.curx = lflush.cury = 0

    if lpoint > 0:
        if EXTRA:
            c.bytesout += lpoint

        if enable_scroll <= -1:
            flush_buf()

            # Catch write errors on save files
            if os.write(Write_fd, lpbuf) != lpoint:
                warn("Error writing output file\n")

            lpnt = 0
            lpbuf.clear()
            return

        it = iter(lpbuf)
        for ch in it:
            if ch >= b' ':
                ttputch(ch)
                lflush.curx += 1
            else:
                # Python has no switch. So if/else here we go!
                if ch == CLEAR:
                    tputs(CL);
                    lflush.curx = 0
                    lflush.cury = 0
                elif ch == CL_LINE:
                    tputs(CE)
                elif ch == CL_DOWN:
                    tputs(CD)
                elif ch == ST_START:
                    tputs(SO)
                elif ch == ST_END:
                    tputs(SE)
                elif ch == CURSOR:
                    lflush.curx = next(it) - 1
                    lflush.cury = next(it) - 1
                    tputs(atgoto(CM, lflush.curx, lflush.cury))
                elif ch == b'\n':
                    if lflush.cury == 23 and enable_scroll:
                        scrline += 1
                        if scrline > 23:
                            scrline = 19
                        
                        tputs(atgoto(CM, 0, scrline + 1))
                        tputs(CE)
                        
                        tputs(atgoto(CM, 0, scrline))
                        tputs(CE)
                        
                    else:
                        ttputch(b'\n')
                        lflush.cury += 1
                    
                    lflush.curx = 0
                elif ch == T_INIT:
                    if TI:
                        tputs(TI)
                elif ch == T_END:
                    if TE:
                        tputs(TE)
                else:   # default:
                    ttputch(ch)
                    lflush.curx += 1
    lpnt = 0
    flush_buf()  # flush real output buffer now 


@export
def lwclose() -> None:
    """ Close output file, flush if needed. """
    lflush()

    if Write_fd > 2:
        os.close(Write_fd)
        Write_fd = 1
    
@export
def lopen(filename) -> int:
    """ Open a file for reading.

        lopen(0) means from the terminal

        Returns -1 if error, otherwise the file descriptor opened.
    """
    global ipoint, iepoint
    ipoint = iepoint = MAXIBUF

    if not filename:
        fd = 0
       
    else:
        try:
            fd = os.open(filename, os.O_RDONLY|os.O_BINARY)
        except OSError as err:
            # NOTE: This also redirects Write_fd, the output fd.
            lwclose()
            Write_fd = 1
            lpnt = 0
            lprintf(f"Error opening file <{filename}> for reading\n")
            lprintf(f"... {str(err)}\n")
            lflush()
            return -1

    return fd
    
@export
def lrclose() -> None:
    """ Close the input file. """

    if fd > 0:
        os.close(fd)
        fd = 0

@export
def lprcat(string: str) -> None:
    """ Append a string to the output buffer. 

        Avoid calls to lprintf (time consuming).
    """
    global lpbuf, lpnt

    if lpnt >= lpend:
        lflush()
    
    lpbuf[lpnt:] = ""
    lpbuf += string
    lpnt = len(lpbuf)


@export
def cursor(col:int, line:int) -> None:
    """ Put cursor at x,y coordinates, starting at 1,1 (ala termcap). """

    if lpnt >= lpend:
        lflush()

    lpbuf += bytearray([CURSOR, col, line])
    lpnt = len(lpbuf)

@export
def cursors() -> None:
    """ Position cursor at beginning of 24th line. """
    cursor(1, 24)


## NOTE: This is a copy of a C comment at this point. It makes little sense:

# Warning: ringing the bell is control code 7. Don't use in defines.
# Don't change the order of these defines.
# Also used in helpfiles. Codes used in helpfiles should be \E[1 to \E[7 with
# obvious meanings.

static()
outbuf = None
""" Translated output buffer """

#
# ANSI control sequences
#

ESC = '\N{ESCAPE}'
CE = ESC +  "[K"
""" Clear to end of line """

CD = None
""" clear to end of display (apparently unimplemented/unsupported)"""

CL = ESC + "[;H" + ESC + "[2J"
""" clear screen """

CM = ESC + "[%i%2;%2H"
""" cursor motion """

static()
AL = ESC + "[L"
""" insert line """

static()
DL = ESC + b'[M'
""" delete line """

static()
SO = ESC + b'[1m'
""" begin standout mode """

static()
SE = ESC + b'[m'
""" end standout mode """

static()
TI = ESC + b'[m'
""" terminal initialization """

static()
TE = ESC + b'[m'
""" terminal end """

@export
def init_term() -> None:
    """ Terminal initialization """
    outbuf = bytearray()
    ansiterm.init()

@export 
def cl_line(col:int, line:int) -> None:
    """ Clear the whole line indicated by 'line' and leave cursor at 
        col,line.
    """
    cursor(1, line)
    lpbuf += CL_LINE
    lpnt = len(lpbuf)
    cursor(col, line)

@export
def cl_up(col, line) -> None:
    """ Clear screen from [col, 1] to current position. Leave cursor at
        [col, line].

        FIXME: The description does not match the code.
    """
    cursor(1, 1)
    
    for i in range(line):
        lpbuf += CL_LINE + b'\n'

    
    cursor(col, line)

@export
def cl_dn(col, line) -> None:
    """ Clear screen from [1, y] to end of display. Leave cursor at 
        [col, line].
    """
    cursor(1, line)
    
    if not CD:
        lpbuf += b'\n'.join([CL_LINE] * (26 - y))
        cursor(col, line)
    else:
        lpbuf += CL_DOWN
    
    cursor(col, line)


@export
def lstandout(string:str) -> None:
    """ Print the argument string in inverse video (standout mode). """
    
    lpbuf += ST_START
    lpbuf += string.encode("utf-8")
    lpbuf += ST_END
    lpnt = len(lpbuf)


@export
def set_score_output() -> None:
    """ Called when output should be literally printed. """
    global enable_scroll
    enable_scroll = -1
    

static()
index :int = 0

@static
def ttputch(ch:int) -> None:
    """ Print one character in decoded output buffer. """

    outbuf.append(ch)
    if len(outbuf) >= BUFBIG:
        flush_buf()

@static
def tputs(cp: str) -> None:
    """ Output string pointed to by cp. """
    if not cp:
        return

    for ch in cp:
        ttputch(ch)



@export
def lflushall() -> None:
    """ Flush all type-ahead in the input buffer. """
    while kbhit():
        getch()


@export
def tmcapcnv(sd: str, ss: str) -> str:
    """ Convert VT100 escapes to termcap format.

        Processes only the ESC-[#m sequence (converts . files for termcap
        use)
    """

    tmstate :int = 0    # 0 = normal, 1=\33 2=[ 3=# 
    tmdigit :int = 0    # the '#' in ESC[#m

    sd = ""

    for ch in ss:
        if tmstate == 0:
            if ch == ESC:
                tmstate += 1
            else:
                sd += ch     # ign:
                tmstate = 0  # ign2:

        elif tmstate == 1:
            if ch == '[':
                tmstate += 1
            else:
                sd += ch
                tmstate = 0

        elif tmstate == 2:
            if ch.isdigit():
                tmdigit = ord(ch) - ord('0')
                tmstate += 1
            else:
                sd += ST_END if ch == 'm' else ch
                tmstate = 0

        elif tmstate == 3:
            if ch == 'm':
                sd += ST_START if tmdigit else ST_END
            else:
                sd += ch

            tmstate = 0
        else:
            sd += ch
            tmstate = 0

    return sd


@static
def warn(msg:str) -> None:
    print(msg, file=sys.stderr)


@export
def enter_name() -> None:
    """  Prompt user for a name. """

    lprcat("\n\nEnter character name:\n")
    sncbr()

    global logname
    logname = ""

    while len(logname) < LOGNAMESIZE - 1:
        ch = ttgetch()
        if ch == '\n':
            break
        logname += ch

    scbr()


@export 
def select_sex() -> None:
    """ Prompt user for character's sex. """

    lprcat("\n\nSelect character sex (0=female,1=male):\n")
    sncbr()
    ch = ttgetch()
    
    if ch == '0':
        sex = 0
    else:
        sex = 1

    scbr()
