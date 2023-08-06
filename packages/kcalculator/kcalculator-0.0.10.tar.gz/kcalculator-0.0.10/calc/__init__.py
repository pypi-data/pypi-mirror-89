# -*- coding: utf-8 -*-

"""
simplecalculator library
-------------------------

This is a proof of concept of a simple calculator library, written in Python.

It mimick the behavior of a very simple desktop calculator. You give it a list
of numbers and operations as a string and it will create a trace of the
operations performed.  That trace is stores in BasicCalculator.log. The most
recent state of the LCD display is stored in Basic Calculator
"""

__title__ = 'calculator'
__version__ = '0.0.10'
__build__ = 0x000003
__author__ = 'kuldeep khatana'
__license__ = 'The MIT License'
__copyright__ = 'Copyright 2020 kuldeep khatana'

from . import calc
