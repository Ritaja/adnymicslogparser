import os

import pip
from setuptools import setup
from pip.req import parse_requirements

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
# def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=pip.download.PipSession())

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name="log parser",
    version="0.0.1",
    author="Ritaja Sengupta",
    author_email="ritaja.sengupta@gmail.com",
    description=("An adnymics task"),
    license="MIT",
    url="http://packages.python.org/logparser.com",
    packages=['adnymicsLogParser'],
    # long_description=read('README'),
    zip_safe=False,
    install_requires=reqs,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: MIT License",
    ],
)
