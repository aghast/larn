import setuptools
import textwrap

#import pprint
#pprint.pprint(setup)

requirements_dev = """
""".strip().split()

requirements_test = """
    mypy
    pytest
    pytest-cov
""".strip().split()


CLASSIFIERS = textwrap.dedent("""
    Development Status :: 2 - Pre-Alpha
    Environment :: Console :: Curses
    Intended Audience :: End Users/Desktop
    License :: Free To Use But Restricted
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: Implementation :: CPython
    Topic :: Games/Entertainment
    Topic :: Games/Entertainment :: Role-Playing
""".strip()).split('\n')

setuptools.setup(
    author='aghast',
    author_email="ah08010-github@yahoo.com",
    classifiers=CLASSIFIERS,
    description='A Python implementation of Larn',
    entry_points={
        'console_scripts': [
            'pylarn=larn:main',
        ],
    },
    install_requires=requirements_dev,
    name='python-larn',
    packages=setuptools.find_packages(),
    package_data={},
    tests_require=requirements_test,
    url="https://github.com/aghast/python-larn",
    version='0.0.1',
    keywords='larn rogue-like',
)

