""" larn/ansiterm.py

    was: ansiterm.c, ansiterm.h

    was: "this is hackjob that translates the ANSI escape sequences used by larn
    to Curses API calls"
"""
import curses

from aghast.util import export, static

stdscr = None

@export
def init():
    """ Initialize curses, and set some basic terminal modes.
    """
    global stdscr

    stdscr = curses.initscr()
    stdscr.notimeout(True)
    curses.noecho()
    curses.cbreak()
    curses.nonl()
    stdscr.keypad(True)

def clean_up():
    curses.nocbreak()
    curses.nl()
    curses.echo()
    curses.endwin()

@export
def out(outbuf: str, n_chars: int) -> None:
    """ writes to the terminal

        Handles escape sequences like these:
        /* 
        ESC[;H 
        ESC[y;xH   ESC[24;01H
        ESC[2J
        ESC[1m standout on
        ESC[m standout off
        */
        
    """
    ANSITERM_ESC = chr(27)

    chit = iter(outbuf)
    for ch in chit:
        if ch != ANSITERM_ESC:
            ansiterm_putchar(ch)
            continue

        # Handle escape sequence
        ansi_param = []
        param1 = param2 = ""

        ch = next(chit)
        while not ch.isalpha():
            ansi_param.append(ch)
            ch = next(chit)

        ansi_cmd = ch

        if ansi_param:
            param1, _, param2 = ''.join(ansi_param).partition(';')

        ansiterm_command(ansi_cmd, param1, param2);


@export
def getch() -> None:
    """ get char
    """
    return llgetch()


@export
def getche() -> int:
    """ get char (with echo)
    """
    curses.echo()
    key = llgetch()
    curses.noecho()
    return key

KEY_REMAP = {
    curses.KEY_UP: 'k',
    curses.KEY_DOWN: 'j',
	curses.KEY_LEFT: 'h',
	curses.KEY_RIGHT: 'l',
	#curses.KEY_A2: 'k',
	#curses.KEY_B1: 'h',
	#curses.KEY_B3: 'l',
	#curses.KEY_C2: 'j',
	#curses.PADENTER: 13,
	curses.KEY_A1: 'y',
	curses.KEY_A3: 'u',
	curses.KEY_C1: 'b',
	curses.KEY_C3: 'n',
	curses.KEY_ENTER: 13, 
}

@static 
def llgetch() -> int:
    """ Get character from the terminal. Translate keypad keys into
        "normal" vi-directional keys.
    """
    key: int = getch()
    key = KEY_REMAP.get(key, key)
    return key

@static
def command(ansi_cmd: int, param1: str, param2: str) -> None:
    """ Translate terminal-command into curses.
    """

    if ansi_cmd == 'H':
        y = int(param1) - 1 if param1 else 0
        x = int(param2) - 1 if param2 else 0
        move(y, x)

    elif ansi_cmd == 'J':
        clear()

    elif ansi_cmd == 'M':
        n_lines = int(param1) if param1 else 1

        for i in range(n_lines):
            move(0, 0)  # FIXME: should one of these 0's be 'i'?
            clrtoeol()

    elif ansi_cmd == 'K':
        clrtoeol()

    elif ansi_cmd == 'm':
        attribute = int(param1) if param1 else 0
        attribute = (curses.A_NORMAL, curses.A_BOLD)[attribute]
		attrset(attribute)

    else:
        print("Unrecognized ansiterm_command: {!r}".format(ansi_cmd), 
                file=sys.stderr)
        sys.exit(2)

@static 
def putchar(ch: int) -> None:
    """ Output a character
    """
    if ch == '\n':
        y, x = stdscr.getyx()
        move(y + 1, 0)

    elif ch == '\t':
        addstr(" " * 4)

    else:	
        addch(ch);
