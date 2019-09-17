import setuptools
import textwrap

requirements = [
    # TODO: package requirements here
]

setuptools.setup(
    name='python-larn',
    version='0.0.1',
    description='A Python implementation of Larn',
    author='aghast',
    author_email="ah08010-github@yahoo.com",
    url="https://github.com/aghast/python-larn",
    packages="larn".strip().split(),
    package_data={},
    entry_points={
        'console_scripts': [
            'pylarn=larn:main',
        ],
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='larn rogue-like',
    classifiers=textwrap.dedent("""
        Development Status :: 2 - Pre-Alpha
        Environment :: Console :: Curses
        Intended Audience :: End Users/Desktop
        License :: Free To Use But Restricted
        Programming Language :: Python :: 3.7
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Games/Entertainment
        Topic :: Games/Entertainment :: Role-Playing
    """.strip()).split('\n'),
)

#import pprint
#pprint.pprint(setup)
