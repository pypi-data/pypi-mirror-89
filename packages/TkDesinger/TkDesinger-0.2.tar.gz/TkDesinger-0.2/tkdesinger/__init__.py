# __init__ file


__author__ = 'FotonPC'
__license__ = 'MIT'
main_doc = \
    """
This module use modify tkinter.dnd as dnd.py in program directory - Drag And Drop
Supported:
Label
Button
Entry
Listbox
Text
Canvas

This program is not best!!!
And this can generate no right code!

WARNING: Height and width is not const value! It can be in px and pt!
"""


__doc__ = """
It is TkDesinger



imported os and sys
function TkDesinger():
	running TkDesinger\\main.py
	
Foton Tkinter Desinger for Python 3 documentation.
#####****** Docs ******######


""" + main_doc


import os
import sys

def TkDesinger():

	script_path = sys.execute + '\\lib\\site-packages\\TkDesinger\\'
	os.chdir(script_path)
	print('WARNING: Choose directory',script_path)
	print('No run TkDesinger with import!')
	print('UNSTABLE MODE!')
	import tkdesinger.main


if __name__ == '__main__':
	import main