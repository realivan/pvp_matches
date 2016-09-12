from setuptools import setup, find_packages
from os.path import join, dirname
from pvp import __version__

setup(
    name='pvp_matches',
    version=__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    entry_points={
        'console_scripts': ['pvp = pvp.core:main']
    },
    test_suite='pvp.tests',
)
