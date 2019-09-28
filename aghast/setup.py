""" aghast/setup.py

    Utility functions for setup.py
"""
from typing import *

from pip._internal.operations.freeze import freeze as pip_freeze
        
def pip_requirements(path: str) -> List[str]:
    """ Parse the requirements out of a pip requirements file. """
    path_list = [path]
    
    while path_list:
        path = path_list.pop(0)

        with open(path) as reqfile:
            lines = reqfile.readlines()

        missing_versions = set()
        results = []

        version_ops = """== >= <= < >""".split()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if any(operator in line for operator in version_ops):
                results.append(line)
                continue

            if line.startswith('-r'):
                # recursive requirements file
                _, subfile = line.split()
                path_list.append(subfile)
                continue

            if line.startswith('-e'):
                # editable repo or path spec
                _, eggname = line.split('#egg=')
                results.append(eggname)
                continue

            # Now we have a line with a package but no version. Add it to
            # the list of needs.
            missing_versions.add(line)

    # Now all recursive files have been parsed. If any packages are missing
    # versions, run `pip freeze` to get the version numbers.

    if missing_versions:
        for line in pip_freeze(exclude_editable=True):
            name, eql, rest = line.partition('==')
            if name in missing_versions:
                results.append(line)

    return results

if __name__ == '__main__':
    reqfile = './requirements-dev.txt'
    versions = pip_requirements(reqfile)
    print('\n'.join(sorted(versions)))
