import sys
import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if sys.version_info < (3, 4):
    sys.exit("Project requires python 3.4 or above")

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
        name="Matlab Usage Stats",
        version="1.0",
        description="Django based Matlab Licence Usage statistics agregator",
        long_description=README,
        url="https://github.com/akshaykhadse/matlab-usage-stats",
        author="Akshay Khadse, Raghav Gupta",
        author_email="akshay621993@gmail.com, raghavgupta0110@gmail.com",
        license="BSD License",
        install_requires=requires,
        packages=find_packages(),
        )
