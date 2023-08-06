from __future__ import absolute_import

__version__ = "1.0.0"

from onepanel.nbextensions.magics import IPythonMagics

def load_ipython_extension(ipython):
    ipython.register_magics(IPythonMagics)
