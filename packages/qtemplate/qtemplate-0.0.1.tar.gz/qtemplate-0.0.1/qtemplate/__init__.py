"""
qtemplate is a command line CLI  service that handles templates
and prompts for data to generate files from dynamic data
"""
import os
from . import template


def get_version():
    with open('VERSION') as f:
        version = f.read()
        return version


name = "qtemplate"
__version__ = get_version()
