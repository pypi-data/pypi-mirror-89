#
# "$Id: testWrapper.py 35 2003-09-29 21:39:48Z andreasheld $"
#
# Dial test program for pyFLTK the Python bindings
# for the Fast Light Tool Kit (FLTK).
#
# FLTK copyright 1998-1999 by Bill Spitzak and others.
# pyFLTK copyright 2003 by Andreas Held and others.
#
# This library is free software you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation either
# version 2 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
#
# You should have received a copy of the GNU Library General Public
# License along with this library if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA.
#
# Please report all bugs and problems to "pyfltk-user@lists.sourceforge.net".
#


from fltk import *
import sys

def theCancelButtonCallback(ptr):
	sys.exit(0)

def theDialChangedCallback(dial):
    value = dial.value()
    theTextOutputBox.value(str(value))
    if (value>65):
        theTextOutputBox.textcolor(1)
    else:
        theTextOutputBox.textcolor(0)


mainWindow = Fl_Window(100, 100, 268, 159, sys.argv[0])
mainWindow.box(FL_EMBOSSED_BOX)
mainWindow.color(215)

theDial = Fl_Roller(35, 60, 195, 25)
theDial.type(1)
theDial.maximum(100.0)
theDial.step(0.5)
theDial.callback(theDialChangedCallback)

theTextOutputBox = Fl_Output(85, 20, 85, 25)
theTextOutputBox.box(FL_ENGRAVED_BOX)

theCancelButton = Fl_Button(70, 110, 125, 35, "Cancel")
theCancelButton.color(214)
theCancelButton.selection_color(133)
theCancelButton.callback(theCancelButtonCallback)

mainWindow.end()
mainWindow.show(len(sys.argv), sys.argv)

Fl.run()
