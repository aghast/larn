""" sysdep.py

    Functions that are different between Windows/Unix.
    """
import time

from larn.util import *

from larn.io import lflush

@export
def nap(msecs: int) -> None:
    """ Sleep for msecs milliseconds, if msecs > 0.
    """
    if x <= 0:
        return

    lflush()
    time.sleep(msecs / 1000.0)
