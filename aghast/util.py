import sys

import inspect

from types import ModuleType
from typing import *


__all__ = """
    export
    static
""".strip().split()

T = TypeVar('T')

@overload
def export(s: str) -> None: ...
@overload
def export(func: Callable[..., T]) -> Callable[..., T]: ...

def export(name_or_callable):
    """ Add an objects name to the containing-module's `__all__` variable.

        See https://stackoverflow.com/a/41895257/4029014
        """
    if callable(name_or_callable):
        # Get the module, find the __all__ global or create it.
        name = name_or_callable.__name__
        mod = sys.modules[name_or_callable.__module__]
        try:
            allvar = mod.__all__
            if name not in allvar:
                allvar.append(name)
        except AttributeError:
            mod.__all__ = [name]

    else:
        # Inspect the stack, find the __all__ global or create it.
        name = name_or_callable
        fi = inspect.stack()[1]
        fglobals = fi.frame.f_globals
        try:
            allvar = fglobals['__all__']
            if name not in allvar:
                allvar.append(name)
        except KeyError:
            fglobals['__all__'] = [name]

    return name_or_callable

def static(decl: T) -> T:
    """ Indicate an object is static by *not* adding it to `__all__`.
    """
    return decl

