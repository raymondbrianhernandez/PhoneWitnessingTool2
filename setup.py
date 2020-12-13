#!/usr/bin/python
from distutils.core import setup
import py2exe

setup(windows=[{"script": "main.py"}],
      options={"py2exe": {"includes": ["bs4",
                                       "PyQt5.QtCore",
                                       "PyQt5.QtGui"]}}
      )
