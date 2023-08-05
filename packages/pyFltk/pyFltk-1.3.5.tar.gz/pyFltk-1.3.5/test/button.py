#
# "$Id: button.py 495 2013-03-30 09:39:45Z andreasheld $"
#
# Button test program for pyFLTK the Python bindings
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

window = None

class MyButton(Fl_Button):
	data = "My Secret Data"
	def __init__(self, x, y, w, h, l):
		Fl_Button.__init__(self, x, y, w, h, l)
		
def beepcb(ptr, widget):
	print("beepcb: ")
	print("  Widget member: ",ptr.data)

def exitcb(ptr, widget):
	sys.exit(0)

window = Fl_Window(100,100,320, 65,"Button")
b1 = MyButton(20,20,80,25, "Beep")

b1.callback(beepcb, window)
b2 = Fl_Button(120,20, 80, 25, "&no op")
b3 = Fl_Button(220,20, 80, 25, "Exit");
b3.callback(exitcb,window)
window.end()
#window.show(len(sys.argv),sys.argv)
window.show()
Fl.run()


