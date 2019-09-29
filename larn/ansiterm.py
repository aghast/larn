""" larn/ansiterm.py

    was: ansiterm.c, ansiterm.h

    was: "this is hackjob that translates the ANSI escape sequences used by larn
    to Curses API calls"
"""
import curses
import sys

from typing import Optional

from aghast.util import export, static

stdscr: curses._CursesWindow

KEY_REMAP = {
    curses.KEY_UP:    ord('k'),
    curses.KEY_DOWN:  ord('j'),
    curses.KEY_LEFT:  ord('h'),
    curses.KEY_RIGHT: ord('l'),
    curses.KEY_A1:    ord('y'),
    curses.KEY_A3:    ord('u'),
    curses.KEY_C1:    ord('b'),
    curses.KEY_C3:    ord('n'),
    curses.KEY_ENTER: 13, 

    # These were behind an ifndef NCURSES_VERSION
    #curses.KEY_A2:   ord('k'),
    #curses.KEY_B1:   ord('h'),
    #curses.KEY_B3:   ord('l'),
    #curses.KEY_C2:   ord('j'),
    #curses.PADENTER: 13,
}

@static 
def llgetch() -> str:
    """ Get character from the terminal. Translate keypad keys into
        "normal" vi-directional keys.
    """
    key: int = stdscr.getch()
    key = KEY_REMAP.get(key, key)
    return chr(key)

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
            putchar(ch)
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

        command(ansi_cmd, param1, param2);


@export
def getch() -> str:
    """ get char
    """
    return llgetch()


@export
def getche() -> str:
    """ get char (with echo)
    """
    curses.echo()
    key = llgetch()
    curses.noecho()
    return key

@static
def command(ansi_cmd: str, param1: str, param2: str) -> None:
    """ Translate terminal-command into curses.
    """
    if ansi_cmd == 'H':
        y = int(param1) - 1 if param1 else 0
        x = int(param2) - 1 if param2 else 0
        stdscr.move(y, x)

    elif ansi_cmd == 'J':
        clear()

    elif ansi_cmd == 'M':
        n_lines = int(param1) if param1 else 1

        for i in range(n_lines):
            stdscr.move(0, 0)  # FIXME: should one of these 0's be 'i'?
            stdscr.clrtoeol()

    elif ansi_cmd == 'K':
        stdscr.clrtoeol()

    elif ansi_cmd == 'm':
        attribute = int(param1) if param1 else 0
        attribute = (curses.A_NORMAL, curses.A_BOLD)[attribute]
        stdscr.attrset(attribute)

    else:
        print("Unrecognized ansiterm_command: {!r}".format(ansi_cmd), 
                file=sys.stderr)
        sys.exit(2)

@static 
def putchar(ch: str) -> None:
    """ Output a character
    """
    if ch == '\n':
        y, x = stdscr.getyx()
        stdscr.move(y + 1, 0)

    elif ch == '\t':
        stdscr.addstr(" " * 4)

    else:    
        stdscr.addch(ch);
